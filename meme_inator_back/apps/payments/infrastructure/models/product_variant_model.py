from datetime import timezone
import uuid
from django.db import models

class ProductVariantModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid7, editable=False)
    internal_sku = models.CharField(max_length=255, unique=True)
    product_type = models.CharField(max_length=50)
    apple_product_id = models.CharField(max_length=255, null=True, blank=True)
    google_product_id = models.CharField(max_length=255, null=True, blank=True)
    stripe_price_id = models.CharField(max_length=255, null=True, blank=True)
    entitlement_codename = models.CharField(max_length=255, null=True, blank=True)
    token_grants_amount = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)