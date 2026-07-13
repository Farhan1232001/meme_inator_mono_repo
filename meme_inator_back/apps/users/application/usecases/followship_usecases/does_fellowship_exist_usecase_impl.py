from uuid import UUID
from apps.users.domain.usecases.followship_usecases.idoes_followship_exist_usecase import IDoesFollowshipExistUsecase
from apps.users.infrastructure.repositories.social_actions_repository import SocialActionsRepository

from uuid import UUID
from apps.users.domain.usecases.followship_usecases.idoes_followship_exist_usecase import IDoesFollowshipExistUsecase
from apps.users.infrastructure.repositories.social_actions_repository import SocialActionsRepository

from core.results import Error, Result, Ok, NotOk

# TODO: Inefficient query, fix. Just have model determine Followship entry exists
class DoesFollowshipExistUsecase(IDoesFollowshipExistUsecase):
    def __init__(self, social_actions_repo: SocialActionsRepository):
        self.social_actions_repo = social_actions_repo

    def execute(self, user_a_id: UUID, user_b_id: UUID) -> Result[bool]:
        try:
            following = self.social_actions_repo.get_following(str(user_a_id))
            for followed in following:
                if followed.id == user_b_id:
                    return Ok(True)
            return Ok(False)  # Not following is not an error
        except Exception as e:
            return Error(
                message="Failed to check follow status",
                static_msg="FOLLOW_CHECK_ERROR",
                exception=e,
                status_code=500
            )