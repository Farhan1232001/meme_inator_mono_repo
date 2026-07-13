from django.db import models
from uuid import uuid7

class FingerprintModel(models.Model):
    fingerprint_id = models.UUIDField(primary_key=True, default=uuid7, editable=False)

    case = models.ForeignKey(
        to='ModerationCaseModel', 
        on_delete=models.DO_NOTHING, 
        db_constraint=False,  # Prevents DB-level foreign key crashes if case is deleted
        null=True
    )

    # Core hash
    fingerprint_hash = models.CharField(unique=True, max_length=64, db_index=True)

    # Additional metadata from ContentFingerprintVo
    content_type = models.CharField(max_length=50)
    policy_routing_key = models.CharField(max_length=255)
    provider_used = models.CharField(max_length=100)
    decision_outcome = models.CharField(max_length=20)
    confidence_score = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['fingerprint_hash', 'created_at']),
            models.Index(fields=['expires_at']),
            models.Index(fields=['case']),
        ]