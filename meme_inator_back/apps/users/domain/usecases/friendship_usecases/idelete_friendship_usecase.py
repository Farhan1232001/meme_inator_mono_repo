from typing import Protocol
from uuid import UUID


class IDeleteFriendshipUsecase(Protocol):
    def execute(self, friendship_id: UUID) -> bool:
        ...

    def execute(self, user_a_id: UUID, user_b_id: UUID) -> bool:
        ...