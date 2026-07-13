from typing import List, Literal
from ninja_extra import api_controller, route
from ninja import Query
from ninja_jwt.authentication import JWTAuth
from django.http import HttpRequest
from core.results import Result


from apps.feeds.application.orchestration.feeds_orchestration import FeedsOrchestration
from apps.profiles.application.dtos.profile_schema import ProfileSchema
from apps.users.application.dtos.change_password_schema import ChangePasswordSchema
from apps.users.application.dtos.change_username_schema import ChangeUsernameSchema
from apps.users.application.dtos.friend_request_action_schema import FriendRequestActionSchema
from apps.users.application.dtos.friend_request_schema import FriendRequestSchema
from apps.users.application.dtos.user_schema import UserSchema
from apps.users.application.dtos.user_settings_schema import UserSettingsSchema
from apps.users.application.dtos.visibility_schema import VisibilitySchema
from apps.users.application.orchestration.users_orchestration import UsersOrchestration
from core.dependency_injections import di

@api_controller('/users', tags=['Users'], permissions=[]) 
class UsersController:
    """
    Controller for User Identity, Settings, Credentials, and Social Actions.
    Delegates logic to UserOrchestrator.
    """

    def __init__(self):
        # Dependency Injection of the Orchestrator
        self._users_orchestration: UsersOrchestration = di.create_users_orchestration()

    # --- 1. Identity & Basic Info ---
    @route.get('/me', response={200: UserSchema}, auth=JWTAuth())
    def get_user_via_token(self, request: HttpRequest):
        """
        Get current user's identity information by decoding JWT token.
        The user is automatically attached to the request by JWTAuth.
        """
        # Extract user from request (JWTAuth attaches the user object)
        user = request.user

        if not user or not hasattr(user, 'id'):
            raise ValueError("Invalid or missing user in request")
        
        # Pass user_id to orchestration layer
        return self._users_orchestration.get_user_via_id(user.id)

    @route.get('/{username}', response={200: UserSchema}, auth=None)
    def get_identity(self, username: str):
        """Get basic identity information of a user."""
        return self._users_orchestration.get_identity(username)

    # --- 2. Profile Management (Self) ---

    @route.put('/profile', response={200: str}, auth=JWTAuth())
    def replace_profile(self, request: HttpRequest, data: ProfileSchema):
        """Fully replace my profile data."""
        return self._users_orchestration.replace_profile(request.user.id, data)

    @route.patch('/profile', response={200: str}, auth=JWTAuth())
    def update_profile(self, request: HttpRequest, data: ProfileSchema):
        """Partially update my profile data."""
        return self._users_orchestration.update_profile(request.user.id, data)

    # --- 3. Account Settings ---

    @route.put('/settings', response={200: str}, auth=JWTAuth())
    def update_settings(self, request: HttpRequest, data: UserSettingsSchema):
        """Update global user settings."""
        return self._users_orchestration.update_settings(request.user.id, data)

    @route.put('/settings/visibility', response={200: str}, auth=JWTAuth())
    def toggle_visibility(self, request: HttpRequest, data: VisibilitySchema):
        """Toggle online visibility."""
        return self._users_orchestration.set_visibility(request.user.id, data.is_online)

    # --- 4. Credentials (Username & Password) ---

    @route.put('/credentials/change-username', response={200: str}, auth=JWTAuth())
    def change_username(self, request: HttpRequest, data: ChangeUsernameSchema):
        """Change username."""
        return self._users_orchestration.change_username(request.user.id, data)

    @route.put('/credentials/change-password', response={200: str}, auth=JWTAuth())
    def change_password(self, request: HttpRequest, data: ChangePasswordSchema):
        """Change password."""
        return self._users_orchestration.change_password(request.user.id, data)

    # --- 5. Social Actions (Following) ---

    @route.post('/{user_id}/follow', response={204: None, 404: dict, 409: dict, 500: dict}, auth=JWTAuth())
    def follow_user(self, request: HttpRequest, user_id: str):
        """Follow a user. Returns 204 on success, 409 if already following."""
        result = self._users_orchestration.follow(request.user.id, user_id)
        return Result.result_parser(
            result=result,
            ok_handler=lambda _: (204, None),
            default_error_message="internal server error: Failed to follow user"
        )

    @route.delete('/{user_id}/unfollow', response={204: None, 404: dict, 409: dict, 500: dict}, auth=JWTAuth())
    def unfollow_user(self, request: HttpRequest, user_id: str):
        """Unfollow a user. Returns 204 on success, 404 if not following."""
        result = self._users_orchestration.unfollow(request.user.id, user_id)
        return Result.result_parser(
            result=result,
            ok_handler=lambda _: (204, None),
            default_error_message="internal server error: Failed to unfollow user"
        )

    @route.get('/followers', response={200: List[UserSchema]}, auth=JWTAuth())
    def get_followers(self, request: HttpRequest):
        """Get my followers."""
        return self._users_orchestration.list_followers(request.user.id)

    @route.get('/following', response={200: List[UserSchema]}, auth=JWTAuth())
    def get_following(self, request: HttpRequest):
        """Get who I am following."""
        return self._users_orchestration.list_following(request.user.id)

    # --- 6. Social Actions (Friend Requests) ---

    @route.post('/{user_id}/friend_request', response={201: str, 400: str}, auth=JWTAuth())
    def send_friend_request(self, request: HttpRequest, user_id: str):
        """Send a friend request to a user."""
        # Note: Exception handling for 400 usually happens in exception handlers 
        # or via logic in the orchestrator returning specific status codes
        return 201, self._users_orchestration.send_friend_req(request.user.id, user_id)

    @route.get('/friend_requests', response={200: List[FriendRequestSchema]}, auth=JWTAuth())
    def get_friend_requests(
        self, 
        request: HttpRequest, 
        type: Literal['incoming', 'outgoing'] = Query('incoming')
    ):
        """Get list of incoming or outgoing friend requests."""
        return self._users_orchestration.list_friend_reqs(request.user.id, type)

    @route.put('/friend_requests/{request_id}', response={200: str, 404: str}, auth=JWTAuth())
    def respond_friend_request(
        self, 
        request: HttpRequest, 
        request_id: str, 
        body: FriendRequestActionSchema
    ):
        """Accept or reject an incoming friend request."""
        return self._users_orchestration.respond_friend_req(request.user.id, request_id, body.action)

    @route.delete('/friend_requests/{request_id}', response={204: None, 404: str}, auth=JWTAuth())
    def cancel_friend_request(self, request: HttpRequest, request_id: str):
        """Cancel an outgoing friend request."""
        self._users_orchestration.cancel_friend_req(request.user.id, request_id)
        return 204, None

    @route.delete('/{user_id}/friend', response={204: None, 404: str}, auth=JWTAuth())
    def remove_friend(self, request: HttpRequest, user_id: str):
        """Remove an existing friend (Unfriend)."""
        self._users_orchestration.unfriend(request.user.id, user_id)
        return 204, None