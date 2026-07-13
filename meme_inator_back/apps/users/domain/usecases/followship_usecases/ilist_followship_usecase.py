from typing import List, Protocol
from uuid import UUID

from apps.users.domain.entities.friendship_entity import FriendshipEntity


class IListFollowshipUsecase(Protocol):
    def execute(self, user_id: UUID) -> List[FriendshipEntity]:
        ...