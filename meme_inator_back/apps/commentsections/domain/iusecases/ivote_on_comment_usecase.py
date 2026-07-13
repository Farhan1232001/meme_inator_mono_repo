

from abc import ABC
from uuid import UUID

from apps.commentsections.domain.enums.vote_action_enum import VoteActionEnum
from core.results import Result


class IVoteOnCommentUsecase(ABC):


    def execute(self, comment_public_id: UUID, voter_user_id: UUID, action: VoteActionEnum) -> Result:
        ...