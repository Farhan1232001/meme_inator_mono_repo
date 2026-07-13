# apps/registration/models.py
import uuid
from django.db import models
from django.utils import timezone


class RegistrationIntentTokenModel(models.Model):
    """
    TODO: Add cleanup cron for expired intents.
    TODO: Add attempts: int
    TODO: Add ip_address or user_agent (for security. )
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid7, editable=False)
    user_id = models.UUIDField(db_index=True)
    token = models.CharField(max_length=128, unique=True, db_index=True)
    expires_at = models.DateTimeField(db_index=True)
    consumed = models.BooleanField(default=False, db_index=False)
    created_at = models.DateTimeField(default=timezone.now, db_index=False)
    consumed_at = models.DateTimeField(null=True, blank=True, db_index=False)

    class Meta:
        indexes = [
            models.Index(fields=["user_id"]),
            models.Index(fields=["token"]),
            models.Index(fields=["expires_at"]),
            # models.Index(fields=["consumed"]),
            # models.Index(fields=["created_at"]),
            # models.Index(fields=["consumed_at"]),
        ]

    def mark_consumed(self):
        self.consumed = True
        self.consumed_at = timezone.now()
        self.save(update_fields=["consumed", "consumed_at"])

    def __str__(self) -> str:
        return f"<RegistrationIntentToken id={self.id} user_id={self.user_id} consumed={self.consumed}>"
