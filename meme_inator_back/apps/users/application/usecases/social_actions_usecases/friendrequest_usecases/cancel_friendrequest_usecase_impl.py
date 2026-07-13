from uuid import UUID
from apps.users.domain.usecases.social_actions_usecases.ifriendrequest_usecases.icancel_friendrequest_usecase import ICancelFriendRequestUsecase
from apps.users.infrastructure.repositories.friend_request_repo import FriendRequestRepository

class CancelFriendRequestUsecase(ICancelFriendRequestUsecase):
    def __init__(self, friend_request_repo: FriendRequestRepository):
        self.friend_request_repo = friend_request_repo

    def execute(self, user_id: UUID, request_id: UUID) -> None:
        self.friend_request_repo.update_status(request_id, "cancelled")