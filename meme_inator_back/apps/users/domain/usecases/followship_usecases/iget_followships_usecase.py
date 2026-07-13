from typing import List, Protocol
from uuid import UUID

from apps.users.domain.entities.followship_entity import FollowShipEntity


class IGetFollowshipsUsecaseByUser(Protocol):
    def execute(self, user_id: UUID) -> List[FollowShipEntity]:
        ...