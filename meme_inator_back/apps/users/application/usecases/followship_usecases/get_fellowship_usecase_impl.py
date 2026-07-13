from uuid import UUID
from datetime import datetime
from apps.users.domain.usecases.followship_usecases.iget_followship_usecase import IGetFellowshipUsecase
from apps.users.infrastructure.repositories.social_actions_repository import SocialActionsRepository
from apps.users.domain.entities.followship_entity import FollowShipEntity

class GetFellowshipUsecaseImpl(IGetFellowshipUsecase):
    def __init__(self, social_actions_repo: SocialActionsRepository):
        self.social_actions_repo = social_actions_repo

    def execute(self, user_a_id: UUID, user_b_id: UUID) -> FollowShipEntity:
        following = self.social_actions_repo.get_following(str(user_a_id))
        for followed in following:
            if followed.id == user_b_id:
                return FollowShipEntity(
                    id=UUID(int=0),
                    user_a=user_a_id,
                    user_b=user_b_id,
                    created_at=datetime.now()
                )
        raise ValueError("Fellowship not found")