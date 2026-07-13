# apps/registration/infrastructure/models/deregistration_intent_challenge_model.py
import uuid
from django.db import models
from django.utils import timezone

class DeregistrationIntentChallengeModel(models.Model):
    """
    TODO: Add cleanup cron for expired intents.
    TODO: Add attempts: int
    TODO: Add ip_address or user_agent (for security. )
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid7, editable=False)
    user_id = models.UUIDField(db_index=True)
    code_hash = models.CharField(max_length=256)  # store hash (not plain code)
    expires_at = models.DateTimeField(db_index=True)
    consumed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    consumed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "deregistration_intent_challenges"
        indexes = [
            models.Index(fields=["user_id"]),
            models.Index(fields=["expires_at"]),
        ]

    def mark_consumed(self):
        self.consumed = True
        self.consumed_at = timezone.now()
        self.save(update_fields=["consumed", "consumed_at"])

    def __str__(self) -> str:
        return f"<DeregistrationIntentChallenge id={self.id} user_id={self.user_id} consumed={self.consumed}>"
