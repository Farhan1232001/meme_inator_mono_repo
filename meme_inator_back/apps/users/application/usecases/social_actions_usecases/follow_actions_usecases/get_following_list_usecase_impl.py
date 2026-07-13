from uuid import UUID
from typing import List
from apps.users.domain.usecases.social_actions_usecases.ifollow_actions_usecases.iget_following_list_usecase import IGetFollowingListUsecase
from apps.users.infrastructure.repositories.social_actions_repository import SocialActionsRepository
from apps.users.domain.entities.user_entity import UserEntity

class GetFollowingListUsecase(IGetFollowingListUsecase):
    def __init__(self, social_actions_repo: SocialActionsRepository):
        self.social_actions_repo = social_actions_repo

    def execute(self, user_id: UUID) -> List[UserEntity]:
        return self.social_actions_repo.get_following(str(user_id))