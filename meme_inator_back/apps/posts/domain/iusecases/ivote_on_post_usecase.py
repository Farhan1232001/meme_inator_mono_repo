# apps/posts/domain/iusecases/ivote_on_post_usecase.py
from abc import ABC, abstractmethod
from uuid import UUID
from apps.commentsections.domain.enums.vote_action_enum import VoteActionEnum
from core.results import Result


class IVoteOnPostUsecase(ABC):
    """Like/Dislike/Remove vote on a post. Idempotent behavior expected from repository.
    
    - Ensures post exists
    - Delegates vote logic to VoteRepository (which should update aggregates atomically)
    - Returns resulting VoteEntity
    """

    @abstractmethod
    def execute(self, post_public_id: UUID, voter_user_id: UUID, action: VoteActionEnum) -> Result:
        ...