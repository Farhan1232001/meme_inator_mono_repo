from uuid import UUID
from apps.users.domain.irepositories.ifriendship_repository import IFriendshipRepository
from apps.users.domain.usecases.friendship_usecases.iget_friendship_usecase import IGetFriendshipUsecase
from apps.users.domain.entities.friendship_entity import FriendshipEntity

class GetFriendshipUsecaseImpl(IGetFriendshipUsecase):
    def __init__(self, friendship_repo: IFriendshipRepository):
        self.friendship_repo = friendship_repo

    def execute(self, user_a_id: UUID, user_b_id: UUID) -> FriendshipEntity:
        friendship = self.friendship_repo.get_by_users(user_a_id, user_b_id)
        if not friendship:
            raise ValueError("Friendship not found")
        return friendship