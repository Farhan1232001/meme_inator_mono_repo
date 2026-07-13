# apps/accounts/infrastructure/models/password_reset_intent_model.py
from uuid import uuid7
from django.db import models
from django.utils import timezone


class PasswordResetIntentModel(models.Model):
    """
    Persistence model for password reset intents.
    Stores a hashed challenge code, expiration, and consumption state.
    TODO: Add cleanup cron for expired intents.
    TODO: Add attempts: int
    TODO: Add ip_address or user_agent (for security. )
    """

    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)

    user_id = models.UUIDField(db_index=True)

    challenge_hash = models.CharField(
        max_length=255,
        help_text="Hashed password reset challenge code",
    )

    expires_at = models.DateTimeField(db_index=True)

    consumed = models.BooleanField(default=False)
    consumed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "password_reset_intents"
        indexes = [
            models.Index(fields=["user_id"]),
            models.Index(fields=["expires_at"]),
            models.Index(fields=["consumed"]),
        ]

    def __str__(self) -> str:
        return f"PasswordResetIntent(user_id={self.user_id}, consumed={self.consumed})"
