
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import UUID, uuid7

from apps.moderation_sys.domain.enums.webhook_enums import WebhookDeliveryStatus, WebhookEventType
from apps.moderation_sys.domain.value_objects.webhook_retry_policy import WebhookRetryPolicyVo


@dataclass
class WebhookDeliveryRecord:
    """
    Tracks a single webhook delivery attempt to an external service.
    """
    record_id: UUID = field(default_factory=uuid7)
    
    # What we're delivering
    event_type: WebhookEventType = None
    payload: Dict[str, Any] = field(default_factory=dict)
    target_url: str = ""
    
    # Delivery tracking
    status: WebhookDeliveryStatus = WebhookDeliveryStatus.PENDING
    attempts: int = 0
    last_attempt_at: Optional[datetime] = None
    next_retry_at: Optional[datetime] = None
    
    # Results
    response_code: Optional[int] = None
    response_body: Optional[str] = None
    error_message: Optional[str] = None
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=datetime.now(timezone.utc))
    delivered_at: Optional[datetime] = None
    expired_at: Optional[datetime] = None
    
    # Related to moderation case
    case_id: Optional[UUID] = None
    policy_routing_key: Optional[str] = None

    def schedule_delivery(self, retry_policy: WebhookRetryPolicyVo) -> None:
        """
        Schedule first delivery attempt.
        Sets status to PENDING and prepares for immediate delivery.
        """
        if self.status not in [WebhookDeliveryStatus.PENDING, WebhookDeliveryStatus.FAILED,
                               WebhookDeliveryStatus.RETRYING]:
            raise ValueError(f"Cannot schedule delivery in status: {self.status}")
        
        self.status = WebhookDeliveryStatus.PENDING
        self.next_retry_at = datetime.now(timezone.utc)  # Ready immediately
        self.updated_at = datetime.now(timezone.utc)

    def mark_success(self, response_code: int, response_body: str = "") -> None:
        """
        Mark webhook as successfully delivered.
        """
        if self.status == WebhookDeliveryStatus.EXPIRED:
            raise ValueError("Cannot mark expired webhook as successful")
        
        self.status = WebhookDeliveryStatus.DELIVERED
        self.response_code = response_code
        self.response_body = response_body
        self.delivered_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
        self.error_message = None

    def mark_failure(self, error_message: str, response_code: Optional[int] = None) -> None:
        """
        Mark webhook delivery as failed and schedule retry if possible.
        """
        if self.status == WebhookDeliveryStatus.EXPIRED:
            raise ValueError("Cannot mark expired webhook as failed")
        
        self.status = WebhookDeliveryStatus.FAILED
        self.attempts += 1
        self.last_attempt_at = datetime.now(timezone.utc)
        self.response_code = response_code
        self.error_message = error_message
        self.updated_at = datetime.now(timezone.utc)
        
        # Don't schedule retry here - let the service decide based on policy

    def expire(self) -> None:
        """
        Mark webhook as expired (exhausted all retries).
        """
        self.status = WebhookDeliveryStatus.EXPIRED
        self.expired_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
        
    def is_ready_for_retry(self) -> bool:
        """
        Check if this webhook is ready for a retry attempt.
        Returns True if status is FAILED and next_retry_at has passed.
        """
        if self.status not in [WebhookDeliveryStatus.FAILED, WebhookDeliveryStatus.RETRYING,
                               WebhookDeliveryStatus.PENDING]:
            return False
        
        if self.next_retry_at is None:
            return False
            
        return datetime.now(timezone.utc) >= self.next_retry_at

    def has_exhausted_retries(self, max_retries: int) -> bool:
        """
        Check if max retries have been exhausted.
        """
        return self.attempts >= max_retries