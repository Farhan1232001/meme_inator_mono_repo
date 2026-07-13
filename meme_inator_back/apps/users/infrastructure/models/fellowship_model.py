from uuid import uuid7
from django.db import models
from django.utils import timezone

from apps.users.infrastructure.models.user_model import UserModel


class FellowshipModel(models.Model):
    """
    Represents a uni‑directional follow relationship between two users.
    
    Graph interpretation:
        - Users are nodes.
        - Each fellowship is a directed edge from `user` (follower) to `followed_user` (followed).
        - A complete directed graph (excluding self‑loops) has n×(n‑1) possible edges.
    """
    id = models.UUIDField(primary_key=True, default=uuid7)
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="following"  # users this user follows
    )
    followed_user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="followers"  # users following this user
    )
    started_at = models.DateTimeField(default=timezone.now)
    is_soft_deleted = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "followed_user"],
                condition=models.Q(is_soft_deleted=False),
                name="unique_active_fellowship"
            ),
            models.CheckConstraint(
                condition=~models.Q(user=models.F("followed_user")),
                name="no_self_fellowship"
            )
        ]
        indexes = [
            models.Index(fields=["user", "is_soft_deleted"]),
            models.Index(fields=["followed_user", "is_soft_deleted"]),
        ]

    def __str__(self):
        return f"{self.user} follows {self.followed_user}"