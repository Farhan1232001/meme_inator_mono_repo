from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

@dataclass
class FriendshipEntity:
    id: UUID
    user: UUID
    friend: UUID
    started_at: datetime

    def is_friends_with(self, user_id: UUID) -> bool:
        return self.user == user_id or self.friend == user_id

    def end_friendship(self):
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)

    @staticmethod
    def are_friends(user_a_id: UUID, user_bid: UUID) -> bool:
        raise NotImplementedError

    def unfriend(self) -> None:
        raise NotImplementedError