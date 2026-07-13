from datetime import datetime
from typing import Optional
from uuid import uuid7
from django.db import models
from django.utils import timezone


class ObjectACLEntryModel(models.Model):
    """
    Per-resource ACL entry that grants a permission to either a user or a role
    for a particular resource instance.
    """
    SUBJECT_USER = "user"
    SUBJECT_ROLE = "role"
    SUBJECT_TYPE_CHOICES = [
        (SUBJECT_USER, "User"),
        (SUBJECT_ROLE, "Role"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    resource_type = models.CharField(max_length=128, db_index=True)  # e.g., "Post", "MemeDraft"
    resource_id = models.UUIDField(db_index=True)
    subject_type = models.CharField(max_length=8, choices=SUBJECT_TYPE_CHOICES)
    subject_id = models.UUIDField(db_index=True)  # user id or role id
    permission_codename = models.CharField(max_length=128, db_index=True)  # e.g., "comment.delete"
    granted_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Object ACL Entry"
        verbose_name_plural = "Object ACL Entries"
        # prevent duplicate identical grants
        constraints = [
            models.UniqueConstraint(
                fields=["resource_type", "resource_id", "subject_type", "subject_id", "permission_codename"],
                name="uniq_object_acl_entry"
            )
        ]
        indexes = [
            models.Index(fields=["resource_type", "resource_id"]),
            models.Index(fields=["subject_type", "subject_id"]),
            models.Index(fields=["permission_codename"]),
        ]

    def __str__(self) -> str:
        return f"ACL({self.resource_type}:{self.resource_id} -> {self.subject_type}:{self.subject_id} :: {self.permission_codename})"

    def is_active(self, now: Optional[datetime] = None) -> bool:
        """Return True if the ACL entry is currently active (not expired)."""
        if now is None:
            now = timezone.now()
        if self.expires_at is None:
            return True
        return self.expires_at > now


