from uuid import UUID
from apps.users.domain.usecases.social_actions_usecases.ifollow_actions_usecases.iget_following_count_usecase import IGetFollowingCountUsecase
from apps.users.infrastructure.repositories.social_actions_repository import SocialActionsRepository

class GetFollowingCountUsecaseImpl(IGetFollowingCountUsecase):
    def __init__(self, social_actions_repo: SocialActionsRepository):
        self.social_actions_repo = social_actions_repo

    def execute(self, user_id: UUID) -> int:
        following = self.social_actions_repo.get_following(str(user_id))
        return len(following)
