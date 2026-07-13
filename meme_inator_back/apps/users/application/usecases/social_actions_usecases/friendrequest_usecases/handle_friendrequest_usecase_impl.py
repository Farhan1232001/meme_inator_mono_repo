from datetime import datetime, timezone
from uuid import UUID, uuid7
from apps.users.domain.enums.friend_request_action import FriendRequestAction
from apps.users.domain.entities.friendship_entity import FriendshipEntity
from apps.users.domain.irepositories.friend_request_repository import IFriendRequestRepository
from apps.users.domain.irepositories.ifriendship_repository import IFriendshipRepository
from apps.users.domain.usecases.social_actions_usecases.ifriendrequest_usecases.ihandle_friendrequest_usecase import IHandleFriendRequestUsecase

class HandleFriendRequestUsecase(IHandleFriendRequestUsecase):
    def __init__(self, friend_request_repo: IFriendRequestRepository, friendship_repo: IFriendshipRepository):
        self.friend_request_repo = friend_request_repo
        self.friendship_repo = friendship_repo

    def execute(self, user_id: UUID, request_id: UUID, action: FriendRequestAction) -> None:
        req = self.friend_request_repo.get_by_id(request_id)
        if not req:
            raise ValueError("Request not found")

        if action == FriendRequestAction.ACCEPT:
            # Accept request
            self.friend_request_repo.update_status(request_id, "accepted")
            # Create friendship
            friendship = FriendshipEntity(
                id=uuid7(),
                user=req.sender_id,
                friend=req.receiver_id,
                started_at=datetime.now(timezone.utc)
            )
            self.friendship_repo.create(friendship)
        elif action == FriendRequestAction.REJECT:
            self.friend_request_repo.update_status(request_id, "rejected")
        else:
            raise ValueError("Invalid action")