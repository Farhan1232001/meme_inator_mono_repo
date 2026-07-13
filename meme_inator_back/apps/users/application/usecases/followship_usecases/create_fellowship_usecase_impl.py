# application/usecases/followship_usecases/create_fellowship_usecase_impl.py
from typing import Protocol
from uuid import UUID
from apps.users.domain.usecases.followship_usecases.icreate_followship_usecase import ICreateFollowshipUsecase
from apps.users.domain.irepositories.social_actions_repository import ISocialActionsRepository

class CreateFellowshipUsecaseImpl(ICreateFollowshipUsecase):
    def __init__(self, social_repo: ISocialActionsRepository):
        self.social_repo = social_repo
    
    def execute(self, user_a_id: UUID, user_b_id: UUID) -> bool:
        try:
            self.social_repo.follow_user(user_a_id, user_b_id)
            return True
        except Exception:
            return False