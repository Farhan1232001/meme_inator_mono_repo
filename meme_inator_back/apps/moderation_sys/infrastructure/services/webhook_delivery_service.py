# infrastructure/services/webhook_delivery_service.py
import httpx
import json
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict, Any
from uuid import UUID

from apps.moderation_sys.domain.aggregates.webhook_delivery_record import WebhookDeliveryRecord
from apps.moderation_sys.domain.enums.webhook_enums import WebhookDeliveryStatus, WebhookEventType
from apps.moderation_sys.domain.irepositories.webhook_delivery_record_repository import IWebhookDeliveryRecordRepository
from apps.moderation_sys.domain.value_objects.webhook_retry_policy import WebhookRetryPolicyVo
from core.results import Result, Ok, NotOk, Error

logger = logging.getLogger(__name__)


class WebhookDeliveryService:
    """
    Service responsible for delivering webhooks to external services.
    Handles retry logic with exponential backoff.
    """
    
    def __init__(
        self,
        webhook_repo: IWebhookDeliveryRecordRepository,
        retry_policy: Optional[WebhookRetryPolicyVo] = None,
        timeout_seconds: int = 30
    ):
        self._webhook_repo = webhook_repo
        self._retry_policy = retry_policy or WebhookRetryPolicyVo()
        self._timeout = timeout_seconds
        
    def create_delivery_record(
        self,
        event_type: WebhookEventType,
        payload: Dict[str, Any],
        target_url: str,
        case_id: Optional[UUID] = None,
        policy_routing_key: Optional[str] = None
    ) -> WebhookDeliveryRecord:
        """
        Create and schedule a new webhook delivery record.
        """
        record = WebhookDeliveryRecord(
            event_type=event_type,
            payload=payload,
            target_url=target_url,
            case_id=case_id,
            policy_routing_key=policy_routing_key
        )
        record.schedule_delivery(self._retry_policy)
        
        saved_record = self._webhook_repo.save(record)
        logger.info(f"Created webhook delivery record {saved_record.record_id} for {event_type}")
        return saved_record
    
    def deliver_single_webhook(self, record_id: UUID) -> Result:
        """
        Attempt to deliver a single webhook.
        Returns Result indicating success or failure.
        """
        record = self._webhook_repo.find_by_id(record_id)
        if not record:
            return NotOk(
                message=f"Webhook record {record_id} not found",
                static_msg="WEBHOOK_NOT_FOUND"
            )
        
        if not record.is_ready_for_retry():
            return NotOk(
                message=f"Webhook {record_id} not ready for delivery",
                static_msg="WEBHOOK_NOT_READY"
            )
        
        try:
            # Attempt HTTP POST delivery
            response = self._send_http_request(record)
            
            if response.status_code in (200, 201, 202, 204):
                # Success!
                record.mark_success(
                    response_code=response.status_code,
                    response_body=response.text[:1000]  # Truncate for storage
                )
                self._webhook_repo.save(record)
                logger.info(f"Webhook {record_id} delivered successfully")
                return Ok(value=record)
            else:
                # HTTP error response
                error_msg = f"HTTP {response.status_code}: {response.text[:200]}"
                return self._handle_failure(record, error_msg, response.status_code)
                
        except httpx.TimeoutException:
            error_msg = f"Request timeout after {self._timeout}s"
            return self._handle_failure(record, error_msg)
            
        except httpx.RequestError as e:
            error_msg = f"Request failed: {str(e)}"
            return self._handle_failure(record, error_msg)
            
        except Exception as e:
            logger.exception(f"Unexpected error delivering webhook {record_id}")
            return Error(
                message=f"Unexpected error: {str(e)}",
                exception=e
            )
    
    def deliver_pending_webhooks(self, limit: int = 50) -> Result:
        """
        Process all webhooks that are ready for delivery/retry.
        Useful for cron jobs or background tasks.
        """
        try:
            ready_records = self._webhook_repo.find_ready_for_delivery(limit=limit)
            
            success_count = 0
            failure_count = 0
            expired_count = 0
            
            for record in ready_records:
                result = self.deliver_single_webhook(record.record_id)
                
                if isinstance(result, Ok):
                    success_count += 1
                elif isinstance(result, NotOk):
                    failure_count += 1
                    if record.has_exhausted_retries(self._retry_policy.max_retries):
                        expired_count += 1
                        
            logger.info(
                f"Webhook batch complete: {success_count} success, "
                f"{failure_count} failed, {expired_count} expired"
            )
            
            return Ok(value={
                "success_count": success_count,
                "failure_count": failure_count,
                "expired_count": expired_count,
                "total_processed": len(ready_records)
            })
            
        except Exception as e:
            logger.exception("Error processing pending webhooks")
            return Error(message=f"Batch delivery failed: {str(e)}", exception=e)
    
    def resend_failed_webhooks(self, hours_back: int = 24) -> Result:
        """
        Resend all failed webhooks from the last N hours.
        Used for manual replay (Business Process #6).
        """
        try:
            since = datetime.now(timezone.utc) - timedelta(hours=hours_back)
            failed_records = self._webhook_repo.find_failed_since(since)
            
            for record in failed_records:
                # Reset retry counter and schedule for immediate delivery
                record.attempts = 0
                record.status = WebhookDeliveryStatus.PENDING
                record.next_retry_at = datetime.now(timezone.utc)
                record.error_message = None
                self._webhook_repo.save(record)
            
            logger.info(f"Reset {len(failed_records)} failed webhooks for replay")
            
            # Immediately try to deliver them
            return self.deliver_pending_webhooks()
            
        except Exception as e:
            logger.exception("Error resending failed webhooks")
            return Error(message=f"Replay failed: {str(e)}", exception=e)
    
    def _send_http_request(self, record: WebhookDeliveryRecord) -> httpx.Response:
        """
        Send the actual HTTP POST request for the webhook.
        """
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "ModerationSystem-Webhook/1.0",
            "X-Webhook-ID": str(record.record_id),
            "X-Webhook-Event": record.event_type.value,
            "X-Webhook-Attempt": str(record.attempts + 1)
        }
        
        with httpx.Client(timeout=self._timeout) as client:
            response = client.post(
                url=record.target_url,
                json=record.payload,
                headers=headers
            )
            return response
    
    def _handle_failure(
        self,
        record: WebhookDeliveryRecord,
        error_message: str,
        response_code: Optional[int] = None
    ) -> NotOk:
        """
        Handle webhook delivery failure with retry logic.
        """
        record.mark_failure(error_message, response_code)
        
        # Check if we've exhausted retries
        if record.has_exhausted_retries(self._retry_policy.max_retries):
            record.expire()
            self._webhook_repo.save(record)
            logger.warning(
                f"Webhook {record.record_id} expired after {record.attempts} attempts. "
                f"Last error: {error_message}"
            )
            return NotOk(
                message=f"Webhook expired after {record.attempts} attempts",
                static_msg="WEBHOOK_EXPIRED"
            )
        
        # Schedule next retry with exponential backoff
        delay = self._retry_policy.get_delay_for_attempt(record.attempts)
        record.next_retry_at = datetime.now(timezone.utc) + timedelta(seconds=delay)
        record.status = WebhookDeliveryStatus.RETRYING
        
        self._webhook_repo.save(record)
        logger.info(
            f"Webhook {record.record_id} failed (attempt {record.attempts}). "
            f"Retry in {delay}s"
        )
        
        return NotOk(
            message=f"Delivery failed. Will retry {record.attempts}/{self._retry_policy.max_retries}",
            static_msg="WEBHOOK_RETRY_SCHEDULED"
        )