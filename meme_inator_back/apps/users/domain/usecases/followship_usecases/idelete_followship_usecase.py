from typing import Protocol
from uuid import UUID


class IDeleteFollowshipUsecase(Protocol):
    def execute(self, fellowship_id: UUID) -> None:
        ...

    def execute(self, user_a_id: UUID, user_b_id: UUID) -> None:
        ...