from typing import List, Literal
from uuid import UUID
from core.results import Result

from apps.users.application.dtos.change_password_schema import ChangePasswordSchema
from apps.users.application.dtos.change_username_schema import ChangeUsernameSchema
from apps.users.application.dtos.friend_request_schema import FriendRequestSchema
from apps.users.application.dtos.user_schema import UserSchema
from apps.users.application.dtos.user_settings_schema import UserSettingsSchema
from apps.users.application.dtos.visibility_schema import VisibilitySchema
from apps.users.application.mapper import user_to_schema

from apps.users.domain.usecases.social_actions_usecases.ifollow_actions_usecases.ifollow_user_usecase import IFollowUserUsecase
from apps.users.domain.usecases.social_actions_usecases.ifollow_actions_usecases.iget_followers_list_usecase import IGetFollowersListUsecase
from apps.users.domain.usecases.social_actions_usecases.ifollow_actions_usecases.iget_following_list_usecase import IGetFollowingListUsecase
from apps.users.domain.usecases.social_actions_usecases.ifollow_actions_usecases.iunfollow_user_usecase import IUnfollowUserUsecase
from apps.users.domain.usecases.user_usecases.get_user_by_token_id import IGetUserByTokenIdUseCase
from apps.users.domain.usecases.user_usecases.get_user_by_username import IGetUserByUsernameUseCase
from apps.users.domain.usecases.social_actions_usecases.ifriendrequest_usecases.isend_friendrequest_usecase import ISendFriendRequestUsecase
from apps.users.domain.usecases.social_actions_usecases.ifriendrequest_usecases.iget_friendrequests_usecase import IGetFriendRequestsUsecase
from apps.users.domain.usecases.social_actions_usecases.ifriendrequest_usecases.ihandle_friendrequest_usecase import IHandleFriendRequestUsecase
from apps.users.domain.usecases.social_actions_usecases.ifriendrequest_usecases.icancel_friendrequest_usecase import ICancelFriendRequestUsecase
from apps.users.domain.usecases.social_actions_usecases.ifriendrequest_usecases.iremove_friendrequest_usecase import IRemoveFriendUsecase


class UsersOrchestration:
    """
    Orchestrates user-related operations by composing domain usecases.
    """
    def __init__(
        self,
        get_user_by_token_id: IGetUserByTokenIdUseCase,
        get_user_by_username: IGetUserByUsernameUseCase,
        follow_user: IFollowUserUsecase,
        unfollow_user: IUnfollowUserUsecase,
        get_followers: IGetFollowersListUsecase,
        get_following: IGetFollowingListUsecase,
        send_friend_request: ISendFriendRequestUsecase,
        get_friend_requests: IGetFriendRequestsUsecase,
        handle_friend_request: IHandleFriendRequestUsecase,
        cancel_friend_request: ICancelFriendRequestUsecase,
        remove_friend: IRemoveFriendUsecase,
        # Additional usecases for profile, settings, credentials can be added here
    ):
        self.get_user_by_token_id = get_user_by_token_id
        self.get_user_by_username = get_user_by_username
        self.follow_user = follow_user
        self.unfollow_user = unfollow_user
        self.get_followers = get_followers
        self.get_following = get_following
        self.send_friend_request = send_friend_request
        self.get_friend_requests = get_friend_requests
        self.handle_friend_request = handle_friend_request
        self.cancel_friend_request = cancel_friend_request
        self.remove_friend = remove_friend

    def get_user_via_id(self, user_id: UUID) -> UserSchema:
        """Get user by ID – used for token-based auth."""
        user_entity = self.get_user_by_token_id.execute(user_id)
        if not user_entity:
            raise ValueError(f"User with id {user_id} not found")
        return user_to_schema(user_entity)

    def get_identity(self, username: str) -> UserSchema:
        user_entity = self.get_user_by_username.execute(username)
        if not user_entity:
            raise ValueError(f"User with username {username} not found")
        return user_to_schema(user_entity)
    
    def follow(self, user_id: UUID, target_id: UUID) -> Result[None]:
        return self.follow_user.execute(user_id, target_id)

    def unfollow(self, user_id: UUID, target_id: UUID) -> Result[None]:
        return self.unfollow_user.execute(user_id, target_id)

    def list_followers(self, user_id: UUID) -> List[UserSchema]:
        followers = self.get_followers.execute(user_id)
        return [user_to_schema(u) for u in followers]

    def list_following(self, user_id: UUID) -> List[UserSchema]:
        following = self.get_following.execute(user_id)
        return [user_to_schema(u) for u in following]

    def send_friend_req(self, user_id: UUID, target_id: UUID) -> None:
        self.send_friend_request.execute(user_id, target_id)

    def list_friend_reqs(self, user_id: UUID, type: Literal['incoming', 'outgoing']) -> List[FriendRequestSchema]:
        # Map the FriendRequestEntity to schema.
        # If FriendRequestEntity only contains IDs, you may need to fetch users separately.
        # This example assumes the usecase returns fully populated entities.
        from apps.users.application.mapper import friend_request_to_schema
        requests = self.get_friend_requests.execute(user_id, type)
        return [friend_request_to_schema(req) for req in requests]

    def respond_friend_req(self, user_id: UUID, request_id: UUID, action: str) -> None:
        from apps.users.domain.enums.friend_request_action import FriendRequestAction
        action_enum = FriendRequestAction(action)
        self.handle_friend_request.execute(user_id, request_id, action_enum)

    def cancel_friend_req(self, user_id: UUID, request_id: UUID) -> None:
        self.cancel_friend_request.execute(user_id, request_id)

    def unfriend(self, user_id: UUID, target_id: UUID) -> None:
        self.remove_friend.execute(user_id, target_id)

    # --- Placeholders for profile and settings (to be implemented) ---
    def replace_profile(self, user_id: str, data):
        raise NotImplementedError("Profile usecase not implemented")

    def update_profile(self, user_id: str, data):
        raise NotImplementedError("Profile usecase not implemented")

    def update_settings(self, user_id: str, data: UserSettingsSchema):
        raise NotImplementedError("Settings usecase not implemented")

    def set_visibility(self, user_id: str, is_online: bool):
        raise NotImplementedError("Visibility usecase not implemented")

    def change_username(self, user_id: str, data: ChangeUsernameSchema):
        raise NotImplementedError("Change username usecase not implemented")

    def change_password(self, user_id: str, data: ChangePasswordSchema):
        raise NotImplementedError("Change password usecase not implemented")