from typing import Protocol
from uuid import UUID


class IDoesFollowshipExistUsecase(Protocol):
    def execute(self, user_a_id: UUID, user_b_id: UUID) -> bool:
        """IMPORTANT: user_a is the profile viewer and user_b is the profile owner!"""
        ...
