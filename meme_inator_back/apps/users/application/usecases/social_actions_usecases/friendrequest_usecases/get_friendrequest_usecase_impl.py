from uuid import UUID
from apps.users.domain.usecases.social_actions_usecases.ifriendrequest_usecases.iget_friendrequest_usecase import IGetFriendRequestUsecase
from apps.users.infrastructure.repositories.friend_request_repo import FriendRequestRepository
from apps.users.domain.entities.friend_request_entity import FriendRequestEntity

class GetFriendRequestUsecaseImpl(IGetFriendRequestUsecase):
    def __init__(self, friend_request_repo: FriendRequestRepository):
        self.friend_request_repo = friend_request_repo

    def execute(self, request_id: UUID) -> FriendRequestEntity:
        request = self.friend_request_repo.get_by_id(request_id)
        if not request:
            raise ValueError("Friend request not found")
        return request