# infrastructure/models/webhook_delivery_record_model.py
from django.db import models
from uuid import uuid7

class WebhookDeliveryRecordModel(models.Model):
    record_id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    case_id = models.UUIDField(db_index=True)
    
    # Webhook details
    webhook_url = models.URLField()
    payload = models.JSONField()
    
    # Policy reference
    policy_id = models.UUIDField()
    max_retries = models.IntegerField(default=5)
    
    # Delivery status
    status = models.CharField(max_length=20, default='PENDING', db_index=True)
    retry_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    last_retry_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    # Error tracking
    last_error = models.TextField(null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['status', 'retry_count']),
            models.Index(fields=['expires_at']),
            models.Index(fields=['case_id']),
        ]