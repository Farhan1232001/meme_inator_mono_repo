from uuid import UUID
from typing import List
from datetime import datetime
from apps.users.domain.usecases.followship_usecases.ilist_followship_usecase import IListFollowshipUsecase
from apps.users.infrastructure.repositories.social_actions_repository import SocialActionsRepository
from apps.users.domain.entities.followship_entity import FollowShipEntity

class ListFollowshipUsecaseImpl(IListFollowshipUsecase):
    def __init__(self, social_actions_repo: SocialActionsRepository):
        self.social_actions_repo = social_actions_repo

    def execute(self, user_id: UUID) -> List[FollowShipEntity]:
        following = self.social_actions_repo.get_following(str(user_id))
        followers = self.social_actions_repo.get_followers(str(user_id))
        fellowships = []
        for followed in following:
            fellowships.append(FollowShipEntity(
                id=UUID(int=0), # int parameter creates nil UUID ie where all 128 bits are set to zero. 
                user_a=user_id,
                user_b=followed.id,
                created_at=datetime.now()
            ))
        for follower in followers:
            fellowships.append(FollowShipEntity(
                id=UUID(int=0),
                user_a=follower.id,
                user_b=user_id,
                created_at=datetime.now()
            ))
        return fellowships