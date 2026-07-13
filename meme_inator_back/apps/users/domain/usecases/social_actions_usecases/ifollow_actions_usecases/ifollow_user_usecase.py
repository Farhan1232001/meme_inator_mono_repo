from typing import Protocol
from uuid import UUID
from core.results import Result


class IFollowUserUsecase(Protocol):
    def execute(self, follower_id: UUID, target_user_id: UUID) -> Result[None]:
        ...