from dataclasses import dataclass, field
from datetime import datetime, timedelta
from uuid import UUID
from apps.users.domain.enums.friend_request_status import FriendRequestStatus

@dataclass
class FriendRequestEntity:
    id: UUID
    sender_id: UUID
    receiver_id: UUID
    created_at: datetime
    status: FriendRequestStatus = FriendRequestStatus.PENDING
    updated_at: datetime = None
    expires_at: datetime = None
    message: str = None

    def __post_init__(self):
        if self.expires_at is None:
            self.expires_at = self.created_at + timedelta(days=7)

    def accept(self, by_user_id: UUID):
        if not self.is_receiver(by_user_id):
            raise ValueError("Only receiver can accept")
        self.status = FriendRequestStatus.ACCEPTED
        self.updated_at = datetime.utcnow()

    def decline(self, by_user_id: UUID):
        if not self.is_receiver(by_user_id):
            raise ValueError("Only receiver can decline")
        self.status = FriendRequestStatus.DECLINED
        self.updated_at = datetime.utcnow()

    def cancel(self, by_user_id: UUID):
        if not self.is_sender(by_user_id):
            raise ValueError("Only sender can cancel")
        self.status = FriendRequestStatus.CANCELLED
        self.updated_at = datetime.utcnow()

    def is_expired(self) -> bool:
        return datetime.utcnow() > self.expires_at

    def is_pending(self) -> bool:
        return self.status == FriendRequestStatus.PENDING

    def is_sender(self, user_id: UUID) -> bool:
        return self.sender_id == user_id

    def is_receiver(self, user_id: UUID) -> bool:
        return self.receiver_id == user_id