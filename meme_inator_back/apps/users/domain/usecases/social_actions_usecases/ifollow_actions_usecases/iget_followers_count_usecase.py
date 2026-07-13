from typing import Protocol
from uuid import UUID


class IGetFollowersCountUsecase(Protocol):
    def execute(self, user_id: UUID) -> int:
        ...
