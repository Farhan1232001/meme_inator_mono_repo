from uuid import UUID
from typing import List
from apps.users.domain.usecases.social_actions_usecases.ifollow_actions_usecases.iget_followers_list_usecase import IGetFollowersListUsecase
from apps.users.infrastructure.repositories.social_actions_repository import SocialActionsRepository
from apps.users.domain.entities.user_entity import UserEntity

class GetFollowersListUsecase(IGetFollowersListUsecase):
    def __init__(self, social_actions_repo: SocialActionsRepository):
        self.social_actions_repo = social_actions_repo

    def execute(self, user_id: UUID) -> List[UserEntity]:
        return self.social_actions_repo.get_followers(str(user_id))