# infrastructure/repositories/django_webhook_delivery_record_repository.py
from uuid import UUID
from typing import Optional, List
from datetime import datetime, timezone

from django.db.models import Q

from apps.moderation_sys.domain.aggregates.webhook_delivery_record import DeliveryStatus, WebhookDeliveryRecord
from apps.moderation_sys.domain.irepositories.webhook_delivery_record_repository import IWebhookDeliveryRecordRepository
from apps.moderation_sys.domain.value_objects.webhook_retry_policy import WebhookRetryPolicyVo
from apps.moderation_sys.infrastructure.models.webhook_delivery_record_model import WebhookDeliveryRecordModel


class DjangoWebhookDeliveryRecordRepository(IWebhookDeliveryRecordRepository):
    
    def save(self, record: WebhookDeliveryRecord) -> WebhookDeliveryRecord:
        """Save or update a webhook delivery record"""
        model, created = WebhookDeliveryRecordModel.objects.update_or_create(
            record_id=record.record_id,
            defaults={
                'case_id': record.case_id,
                'webhook_url': record.webhook_url,
                'payload': record.payload,
                'policy_id': record.policy_id,
                'max_retries': record.max_retries,
                'status': record.status.value,
                'retry_count': record.retry_count,
                'created_at': record.created_at,
                'last_retry_at': record.last_retry_at,
                'expires_at': record.expires_at,
                'delivered_at': record.delivered_at,
                'last_error': record.last_error,
            }
        )
        return self._to_domain(model)
    
    def find_by_id(self, record_id: UUID) -> Optional[WebhookDeliveryRecord]:
        """Find webhook delivery record by ID"""
        try:
            model = WebhookDeliveryRecordModel.objects.get(record_id=record_id)
            return self._to_domain(model)
        except WebhookDeliveryRecordModel.DoesNotExist:
            return None
    
    def find_failed_ready_for_retry(self, limit: int = 100) -> List[WebhookDeliveryRecord]:
        """Find failed records that are ready for retry"""
        now = datetime.now(timezone.utc)
        models = WebhookDeliveryRecordModel.objects.filter(
            status='PENDING',
            retry_count__lt=models.F('max_retries')
        ).filter(
            Q(expires_at__isnull=True) | Q(expires_at__gt=now)
        ).order_by('created_at')[:limit]
        
        return [self._to_domain(model) for model in models]
    
    def find_by_status(self, status: str, limit: int = 100) -> List[WebhookDeliveryRecord]:
        """Find records by delivery status"""
        models = WebhookDeliveryRecordModel.objects.filter(
            status=status
        ).order_by('-created_at')[:limit]
        
        return [self._to_domain(model) for model in models]
    
    def find_expired(self) -> List[WebhookDeliveryRecord]:
        """Find expired records that haven't been delivered"""
        now = datetime.now(timezone.utc)
        models = WebhookDeliveryRecordModel.objects.filter(
            status='PENDING',
            expires_at__lte=now
        )
        
        return [self._to_domain(model) for model in models]
    
    def find_by_case_id(self, case_id: UUID) -> List[WebhookDeliveryRecord]:
        """Find all webhook deliveries for a specific moderation case"""
        models = WebhookDeliveryRecordModel.objects.filter(
            case_id=case_id
        ).order_by('-created_at')
        
        return [self._to_domain(model) for model in models]
    
    def mark_as_expired(self, older_than: datetime) -> int:
        """Mark old pending records as expired, returns count updated"""
        count = WebhookDeliveryRecordModel.objects.filter(
            status='PENDING',
            created_at__lt=older_than
        ).update(
            status='EXPIRED',
            expires_at=datetime.now(timezone.utc)
        )
        return count
    
    def _to_domain(self, model: WebhookDeliveryRecordModel) -> WebhookDeliveryRecord:
        """Convert model to domain aggregate"""
        record = WebhookDeliveryRecord(
            record_id=model.record_id,
            case_id=model.case_id,
            webhook_url=model.webhook_url,
            payload=model.payload,
            policy_id=model.policy_id,
            max_retries=model.max_retries,
            status=DeliveryStatus(model.status),
            retry_count=model.retry_count,
            created_at=model.created_at,
            last_retry_at=model.last_retry_at,
            expires_at=model.expires_at,
            delivered_at=model.delivered_at,
            last_error=model.last_error
        )
        
        # Reconstruct policy if needed
        if hasattr(model, 'policy') and model.policy:
            webhook_policy_data = model.policy.webhook_retry_policy
            record.policy_definition = WebhookRetryPolicyVo(
                max_retries=webhook_policy_data.get('max_retries', 5),
                initial_delay_seconds=webhook_policy_data.get('initial_delay_seconds', 60),
                backoff_multiplier=webhook_policy_data.get('backoff_multiplier', 2.0),
                max_delay_seconds=webhook_policy_data.get('max_delay_seconds', 3600)
            )
        
        return record