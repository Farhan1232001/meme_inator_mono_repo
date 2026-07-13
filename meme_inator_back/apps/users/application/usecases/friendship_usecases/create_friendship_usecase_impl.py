from uuid import UUID
from apps.users.domain.usecases.friendship_usecases.icreate_friendship_usecase import ICreateFriendshipUsecase

class CreateFriendshipUsecaseImpl(ICreateFriendshipUsecase):
    def execute(self, user_a_id: UUID, user_b_id: UUID) -> bool:
        raise NotImplementedError("Use accept_friendrequest instead")