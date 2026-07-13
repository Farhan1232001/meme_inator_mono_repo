from uuid import UUID
from typing import List
from apps.users.domain.entities.friendship_entity import FriendshipEntity
from apps.users.domain.irepositories.ifriendship_repository import IFriendshipRepository
from apps.users.domain.usecases.friendship_usecases.ilist_friendship_usecase import IListFriendshipsUsecase

class ListFriendshipUsecaseImpl(IListFriendshipsUsecase):
    def __init__(self, friendship_repo: IFriendshipRepository):
        self.friendship_repo = friendship_repo

    def execute(self, user_id: UUID) -> List[FriendshipEntity]:
        raise NotImplementedError('')