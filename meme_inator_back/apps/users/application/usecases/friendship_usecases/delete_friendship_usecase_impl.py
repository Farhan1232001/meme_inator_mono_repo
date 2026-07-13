from uuid import UUID
from apps.users.domain.irepositories.ifriendship_repository import IFriendshipRepository
from apps.users.domain.usecases.friendship_usecases.idelete_friendship_usecase import IDeleteFriendshipUsecase

class DeleteFriendshipUsecaseImpl(IDeleteFriendshipUsecase):
    def __init__(self, friendship_repo: IFriendshipRepository):
        self.friendship_repo = friendship_repo

    def execute(self, user_a_id: UUID, user_b_id: UUID) -> bool:
        raise NotImplementedError()