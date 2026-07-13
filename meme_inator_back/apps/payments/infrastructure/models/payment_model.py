from datetime import timezone
import uuid
from django.db import models


class PaymentModel(models.Model):
    # 1. Identity and ownership
    id = models.UUIDField(primary_key=True, default=uuid.uuid7, editable=False)
    user_id = models.UUIDField()

    # 2. Financial Data
    amt_cents = models.BigIntegerField()
    currency = models.CharField(max_length=10)
    status = models.CharField(max_length=50)

    # 3. Provider Linking (For Idempotency & Troubleshooting)
    provider = models.CharField(max_length=50)
    provider_transaction_id = models.CharField(max_length=255, db_index=True)
    provider_original_id = models.CharField(max_length=255, null=True, blank=True)

    # 4. Product metadata
    product_sku = models.CharField(max_length=255)

    # 5. Audit Timestamp
    created_at = models.DateTimeField(default=timezone.now)

    # raw_response = models.JSONField(null=True, blank=True)


    class Meta:
        # Constraint prevents race condition issue
        # If two webhooks for the SAME transaction hit server at same time, 
        # both might pass the find_by_provider_transaction_id check simultaneously 
        # before either has finished the save().
        constraints = [
            models.UniqueConstraint(
                fields=['provider', 'provider_transaction_id'], 
                name='unique_provider_tx'
            )
        ]