from uuid import UUID
from apps.users.domain.usecases.social_actions_usecases.ifriendrequest_usecases.isend_friendrequest_usecase import ISendFriendRequestUsecase
from apps.users.infrastructure.repositories.friend_request_repo import FriendRequestRepository

class SendFriendRequestUsecase(ISendFriendRequestUsecase):
    def __init__(self, friend_request_repo: FriendRequestRepository):
        self.friend_request_repo = friend_request_repo

    def execute(self, sender_id: UUID, target_user_id: UUID) -> None:
        self.friend_request_repo.create_friend_request(sender_id, target_user_id)