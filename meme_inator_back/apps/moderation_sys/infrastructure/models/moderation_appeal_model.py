from uuid import uuid7
from django.db import models
from django.utils.timezone import now

class AppealStatusChoices(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    APPROVED = 'APPROVED', 'Approved'
    DENIED = 'DENIED', 'Denied'
    EXPIRED = 'EXPIRED', 'Expired'

class ModerationAppealModel(models.Model):
    appeal_id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    submitted_by = models.UUIDField(null=False)
    reason = models.TextField()
    submitted_at = models.DateTimeField(default=now)
    status = models.CharField(
        max_length=10,
        choices=AppealStatusChoices.choices,
        default=AppealStatusChoices.PENDING,
    )

