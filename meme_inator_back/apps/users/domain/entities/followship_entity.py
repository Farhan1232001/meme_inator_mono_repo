
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID



@dataclass
class FollowShipEntity:
    id: UUID
    user_a: UUID
    user_b: UUID
    created_at: datetime

    # Getter
    def get_created_at(self) -> datetime:
        return self.created_at

    # Other behaviors
    @staticmethod
    def a_follows_b(user_a: UUID, user_b: UUID) -> bool:
        raise NotImplementedError
    
    @staticmethod
    def b_follows_a(user_a: UUID, user_b: UUID) -> bool:
        raise NotImplementedError
    
    @staticmethod
    def mutual_followers(user_a: UUID, user_b: UUID) -> bool:
        return FollowShipEntity.a_follows_b(user_a,user_b) and FollowShipEntity.b_follows_a(user_a,user_b)

    def to_notification_payload(self) -> dict:
        raise NotImplementedError


