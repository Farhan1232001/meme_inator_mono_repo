from django.db import models
from uuid import uuid7

from apps.moderation_sys.infrastructure.models.moderation_case_model import ModerationCaseModel

class ModerationAttemptModel(models.Model):
    attempt_id = models.UUIDField(primary_key=True, default=uuid7)
    case = models.ForeignKey(
        ModerationCaseModel,
        on_delete=models.CASCADE,
        related_name='attempts'         # case.attempts.all()
    )

    moderator_id = models.CharField(max_length=255, blank=True, null=True)
    decision = models.CharField(max_length=20)
    note = models.TextField(blank=True, null=True)
    attempted_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    resolution_note = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['case']),
            models.Index(fields=['moderator_id']),
        ]