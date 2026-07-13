from typing import List, Protocol
from uuid import UUID

from apps.users.domain.entities.user_entity import UserEntity


class IGetFollowingListUsecase(Protocol):
    def execute(self, user_id: UUID) -> List[UserEntity]:
        ...
