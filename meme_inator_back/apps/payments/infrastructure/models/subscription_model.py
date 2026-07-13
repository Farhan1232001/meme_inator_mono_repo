from datetime import timezone
import uuid
from django.db import models

class SubscriptionModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid7, editable=False)
    user_id = models.UUIDField()
    status = models.CharField(max_length=50)
    product_sku = models.CharField(max_length=255)
    current_period_start = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    cancel_at_period_end = models.BooleanField(default=False)
    provider = models.CharField(max_length=50)
    provider_subscription_id = models.CharField(max_length=255, db_index=True)
    raw_response = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
