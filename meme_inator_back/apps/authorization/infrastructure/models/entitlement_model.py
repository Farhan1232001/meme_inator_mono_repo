# apps/authorization/models.py

from __future__ import annotations
from uuid import uuid4, uuid7
from typing import Optional
from datetime import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone


class EntitlementModel(models.Model):
    """
    Represents a user entitlement (paid grant, promo, internal grant, etc.)

    NOTE: We enforce a uniqueness constraint to avoid duplicate entitlements.
    The current constraint is (user, code, source) — adjust if you prefer
    (user, code) uniqueness instead.
    """
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="entitlements")
    code = models.CharField(max_length=128, db_index=True)  # e.g. "pro_memer"
    source = models.CharField(max_length=64)  # e.g. "stripe", "apple", "google", "promo"
    granted_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(null=True, blank=True)
    meta_data = models.JSONField(default=dict, blank=True)  # store provider metadata (order_id, tokens, etc.)
    # optional bookkeeping
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Entitlement"
        verbose_name_plural = "Entitlements"
        # enforce uniqueness to prevent duplicate entitlements for the same user/code/source
        constraints = [
            models.UniqueConstraint(fields=["user", "code", "source"], name="uniq_entitlement_user_code_source")
        ]
        indexes = [
            models.Index(fields=["user", "code"]),
            models.Index(fields=["code"]),
        ]

    def __str__(self) -> str:
        return f"Entitlement(user={self.user_id}, code={self.code}, source={self.source})"

    def is_active(self, now: Optional[datetime] = None) -> bool:
        """Return True if entitlement is currently active (not expired)."""
        if now is None:
            now = timezone.now()
        if self.expires_at is None:
            return True
        return self.expires_at > now


