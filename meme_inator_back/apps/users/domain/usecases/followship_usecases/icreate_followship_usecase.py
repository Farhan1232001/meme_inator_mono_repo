from typing import Protocol
from uuid import UUID


class ICreateFollowshipUsecase(Protocol):
    def execute(self, user_a_id: UUID, user_b_id: UUID) -> bool:
        ...