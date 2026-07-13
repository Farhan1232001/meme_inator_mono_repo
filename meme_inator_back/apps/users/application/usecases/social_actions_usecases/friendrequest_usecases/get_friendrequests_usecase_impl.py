from uuid import UUID
from typing import List
from apps.users.domain.usecases.social_actions_usecases.ifriendrequest_usecases.iget_friendrequests_usecase import IGetFriendRequestsUsecase
from apps.users.domain.enums.friend_request_type import FriendRequestType
from apps.users.infrastructure.repositories.friend_request_repo import FriendRequestRepository
from apps.users.domain.entities.friend_request_entity import FriendRequestEntity

class GetFriendRequestsUsecase(IGetFriendRequestsUsecase):
    def __init__(self, friend_request_repo: FriendRequestRepository):
        self.friend_request_repo = friend_request_repo

    def execute(self, user_id: UUID, type: FriendRequestType) -> List[FriendRequestEntity]:
        if type == FriendRequestType.INCOMING:
            return self.friend_request_repo.list_received_requests(user_id)
        else:
            return self.friend_request_repo.list_sent_requests(user_id)