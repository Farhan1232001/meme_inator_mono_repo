from typing import Protocol
from uuid import UUID


class IGetFollowingCountUsecase(Protocol):
    def execute(self, user_id: UUID) -> int:
        ...