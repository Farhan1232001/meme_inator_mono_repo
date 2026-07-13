from uuid import UUID
from apps.users.domain.usecases.social_actions_usecases.ifriendrequest_usecases.idoes_friendrequest_exist_usecase import IDoesFriendRequestExistUsecase
from apps.users.infrastructure.repositories.friend_request_repo import FriendRequestRepository

class DoesFriendRequestExistUsecaseImpl(IDoesFriendRequestExistUsecase):
    def __init__(self, friend_request_repo: FriendRequestRepository):
        self.friend_request_repo = friend_request_repo

    def execute(self, user1_id: UUID, user2_id: UUID) -> bool:
        return self.friend_request_repo.exists_between(user1_id, user2_id)