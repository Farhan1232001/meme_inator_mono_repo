from uuid import UUID
from apps.users.domain.usecases.social_actions_usecases.ifollow_actions_usecases.iget_followers_count_usecase import IGetFollowersCountUsecase
from apps.users.infrastructure.repositories.social_actions_repository import SocialActionsRepository

class GetFollowersCountUsecaseImpl(IGetFollowersCountUsecase):
    def __init__(self, social_actions_repo: SocialActionsRepository):
        self.social_actions_repo = social_actions_repo

    def execute(self, user_id: UUID) -> int:
        followers = self.social_actions_repo.get_followers(str(user_id))
        return len(followers)