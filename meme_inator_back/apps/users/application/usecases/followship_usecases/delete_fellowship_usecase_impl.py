from uuid import UUID
from apps.users.domain.usecases.followship_usecases.idelete_followship_usecase import IDeleteFollowshipUsecase
from apps.users.infrastructure.repositories.social_actions_repository import SocialActionsRepository

class DeleteFellowshipUsecaseImpl(IDeleteFollowshipUsecase):
    def __init__(self, social_actions_repo: SocialActionsRepository):
        self.social_actions_repo = social_actions_repo

    def execute(self, user_a_id: UUID, user_b_id: UUID) -> None:
        self.social_actions_repo.unfollow_user(str(user_a_id), str(user_b_id))
