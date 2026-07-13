from uuid import uuid7
from django.db import models
from django.utils import timezone

from apps.users.infrastructure.models.user_model import UserModel


class FriendshipModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7)
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="friendships"
    )
    friend = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="friends_with"
    )
    started_at = models.DateTimeField(default=timezone.now)
    is_soft_deleted = models.BooleanField(default=False)  

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "friend"],
                condition=models.Q(is_soft_deleted=False), 
                name="unique_active_friendship"
            ),
            models.CheckConstraint(
                condition=~models.Q(user=models.F("friend")),
                name="no_self_friendship"
            )
        ]
        indexes = [
            models.Index(fields=["user", "is_soft_deleted"]), 
            models.Index(fields=["friend", "is_soft_deleted"]),  
        ]