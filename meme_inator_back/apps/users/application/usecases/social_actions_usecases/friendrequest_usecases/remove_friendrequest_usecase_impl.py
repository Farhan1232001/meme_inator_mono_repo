from uuid import UUID
from apps.users.domain.irepositories.ifriendship_repository import IFriendshipRepository
from apps.users.domain.usecases.social_actions_usecases.ifriendrequest_usecases.iremove_friendrequest_usecase import IRemoveFriendUsecase
from apps.users.infrastructure.repositories.friend_request_repo import FriendRequestRepository

class RemoveFriendUsecase(IRemoveFriendUsecase):
    def __init__(self, friendship_repo: IFriendshipRepository, friend_request_repo: FriendRequestRepository):
        self.friendship_repo = friendship_repo
        self.friend_request_repo = friend_request_repo

    def execute(self, user_id: UUID, target_user_id: UUID) -> None:
        # End the friendship (if exists)
        friendship = self.friendship_repo.get_by_users(user_id, target_user_id)
        if friendship:
            self.friendship_repo.end_friendship(friendship.id)

        # Delete any pending friend requests between them
        self.friend_request_repo.delete_request_between(user_id, target_user_id)  # you may need to add this method