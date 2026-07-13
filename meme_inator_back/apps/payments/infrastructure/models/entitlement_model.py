from datetime import timezone
import uuid
from django.db import models

class EntitlementModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid7, editable=False)
    user_id = models.UUIDField(db_index=True)
    codename = models.CharField(max_length=255)
    granted_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=100)
    raw_response = models.JSONField(null=True, blank=True)