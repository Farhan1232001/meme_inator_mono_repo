from uuid import UUID
from apps.users.domain.usecases.social_actions_usecases.ifollow_actions_usecases.iunfollow_user_usecase import IUnfollowUserUsecase
from apps.users.infrastructure.repositories.social_actions_repository import SocialActionsRepository
from core.results import Result

class UnfollowUserUsecase(IUnfollowUserUsecase):
    def __init__(self, social_actions_repo: SocialActionsRepository):
        self.social_actions_repo = social_actions_repo

    def execute(self, follower_id: UUID, target_user_id: UUID) -> Result[None]:
        return self.social_actions_repo.unfollow_user(str(follower_id), str(target_user_id))