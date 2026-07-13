from django.db import models
from apps.users.domain.enums.friend_request_status import FriendRequestStatus

class FriendRequestModel(models.Model):
    class Status(models.TextChoices):
        PENDING = FriendRequestStatus.PENDING.value, "Pending"
        ACCEPTED = FriendRequestStatus.ACCEPTED.value, "Accepted"
        DECLINED = FriendRequestStatus.DECLINED.value, "Declined"
        CANCELLED = FriendRequestStatus.CANCELLED.value, "Cancelled"
        EXPIRED = FriendRequestStatus.EXPIRED.value, "Expired"

    sender = models.ForeignKey(
        "UserModel",
        on_delete=models.CASCADE,
        related_name="sent_friend_requests",
    )
    receiver = models.ForeignKey(
        "UserModel",
        on_delete=models.CASCADE,
        related_name="received_friend_requests",
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # track last change
    expires_at = models.DateTimeField(null=True, blank=True)  # auto‑expiry

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["sender", "receiver"],
                condition=models.Q(status__in=[FriendRequestStatus.PENDING, FriendRequestStatus.ACCEPTED]),
                name="unique_active_friend_request"
            ),
        ]
        indexes = [
            models.Index(fields=["sender"]),
            models.Index(fields=["receiver"]),
            models.Index(fields=["status"]),
        ]
    def __str__(self):
        return f"FriendRequest({self.sender} -> {self.receiver}) status={self.status}"
