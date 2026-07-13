from typing import Protocol
from uuid import UUID

from apps.users.domain.entities.followship_entity import FollowShipEntity


class IGetFollowshipUsecaseByUsers(Protocol):
    def execute(self, user_a_id: UUID, user_b_id: UUID) -> FollowShipEntity:
        ...