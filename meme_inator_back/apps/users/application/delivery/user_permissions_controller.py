# apps/users/application/delivery/users_me_controller.py
from typing import List
from uuid import UUID

from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth
from django.http import HttpRequest
from ninja import UploadedFile, File, Query

from core.results import Result
from core.dtos.results_schemas import ErrorResponseSchema
from core.dependency_injections import di

# NOTE: the DTO/schema names below assume you will create them under apps.users.application.dtos.schemas
from apps.users.application.dtos.schemas import (
    UserResponseSchema,
    UpdateUserRequestSchema,
    ChangePasswordRequestSchema,
    UserSettingsResponseSchema,
    UpdateUserSettingsRequestSchema,
    EntitlementsListResponseSchema,
    FollowersListResponseSchema,
    FollowingListResponseSchema,
    NotificationListResponseSchema,
    SessionsListResponseSchema,
    DevicesListResponseSchema,
)

from apps.authorization.application.dtos.schemas import (
    PermissionsListResponseSchema,
    CanPermissionResponseSchema,
    RoleResponseSchema,
)
# ******************************************************************
# *********** WARNING: AI Generated. Code NOT Validated! ***********
# ******** File has NOT been integrated with rest of system *********
# ******************************************************************
@api_controller('/users', tags=['users'])
class UsersMeController:
    """
    Self-service `/users/me/*` endpoints. Keep user-facing convenience endpoints here.
    """

    def __init__(self):
        self.user_orchestration = di.create_user_orchestration()
        self.authz_orchestration = di.create_authorization_orchestration()

    # ---------------- Profile / identity ----------------
    @route.get('/me', auth=JWTAuth(), response={200: UserResponseSchema, 401: ErrorResponseSchema})
    def get_me(self, request: HttpRequest):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result: Result = self.user_orchestration.get_profile(user.id)
        return Result.result_parser(
            result=result,
            ok_handler=lambda u: (200, UserResponseSchema.from_orm(u)),
            default_error_message="internal server error",
        )

    @route.patch('/me', auth=JWTAuth(), response={200: UserResponseSchema, 400: ErrorResponseSchema})
    def update_me(self, request: HttpRequest, payload: UpdateUserRequestSchema):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result: Result = self.user_orchestration.update_profile(user.id, payload)
        return Result.result_parser(
            result=result,
            ok_handler=lambda u: (200, UserResponseSchema.from_orm(u)),
            default_error_message="failed to update profile",
        )

    # ---------------- Credentials ----------------
    @route.patch('/me/password', auth=JWTAuth(), response={204: None, 400: ErrorResponseSchema})
    def change_password(self, request: HttpRequest, payload: ChangePasswordRequestSchema):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result: Result = self.user_orchestration.change_password(user.id, payload.current_password, payload.new_password)
        return Result.result_parser(result=result, ok_handler=lambda _: (204, None), default_error_message="failed to change password")

    @route.patch('/me/username', auth=JWTAuth(), response={200: UserResponseSchema, 400: ErrorResponseSchema})
    def change_username(self, request: HttpRequest, payload):
        # reuse existing orchestrator method if available (change_username)
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result: Result = self.user_orchestration.change_username(user.id, payload)
        return Result.result_parser(result=result, ok_handler=lambda u: (200, UserResponseSchema.from_orm(u)), default_error_message="failed to change username")

    # ---------------- Avatar / media ----------------
    @route.post('/me/avatar', auth=JWTAuth(), response={200: UserResponseSchema, 400: ErrorResponseSchema})
    def upload_avatar(self, request: HttpRequest, file: UploadedFile = File(...)):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result: Result = self.user_orchestration.upload_avatar(user.id, file)
        return Result.result_parser(result=result, ok_handler=lambda u: (200, UserResponseSchema.from_orm(u)), default_error_message="failed to upload avatar")

    @route.delete('/me/avatar', auth=JWTAuth(), response={204: None, 400: ErrorResponseSchema})
    def delete_avatar(self, request: HttpRequest):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result: Result = self.user_orchestration.delete_avatar(user.id)
        return Result.result_parser(result=result, ok_handler=lambda _: (204, None), default_error_message="failed to delete avatar")

    # ---------------- Settings & preferences ----------------
    @route.get('/me/settings', auth=JWTAuth(), response={200: UserSettingsResponseSchema})
    def get_settings(self, request: HttpRequest):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result: Result = self.user_orchestration.get_settings(user.id)
        return Result.result_parser(result=result, ok_handler=lambda s: (200, UserSettingsResponseSchema.from_orm(s)), default_error_message="failed to get settings")

    @route.patch('/me/settings', auth=JWTAuth(), response={200: UserSettingsResponseSchema})
    def update_settings(self, request: HttpRequest, payload: UpdateUserSettingsRequestSchema):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result: Result = self.user_orchestration.update_settings(user.id, payload)
        return Result.result_parser(result=result, ok_handler=lambda s: (200, UserSettingsResponseSchema.from_orm(s)), default_error_message="failed to update settings")

    @route.patch('/me/settings/visibility', auth=JWTAuth(), response={200: UserSettingsResponseSchema})
    def set_visibility(self, request: HttpRequest, is_online: bool = Query(...)):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result: Result = self.user_orchestration.set_visibility(user.id, is_online)
        return Result.result_parser(result=result, ok_handler=lambda s: (200, UserSettingsResponseSchema.from_orm(s)), default_error_message="failed to set visibility")

    # ---------------- Permissions / roles (UI-facing read-only) ----------------
    @route.get('/me/permissions', auth=JWTAuth(), response={200: PermissionsListResponseSchema})
    def my_permissions(self, request: HttpRequest):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result = self.authz_orchestration.get_user_permissions(user.id)
        return Result.result_parser(result=result, ok_handler=lambda perms: (200, PermissionsListResponseSchema(permissions=perms)))

    @route.get('/me/effective_permissions', auth=JWTAuth(), response={200: PermissionsListResponseSchema})
    def my_effective_permissions(self, request: HttpRequest):
        # you have ComputeEffectivePermissionsUseCase; expose it here or call orchestration that wraps it
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result = self.authz_orchestration.compute_effective_permissions(user.id)
        return Result.result_parser(result=result, ok_handler=lambda perms: (200, PermissionsListResponseSchema(permissions=perms)))

    @route.get('/me/roles', auth=JWTAuth(), response={200: List[RoleResponseSchema]})
    def my_roles(self, request: HttpRequest):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        roles_result = self.authz_orchestration.get_user_roles(user.id)
        return Result.result_parser(result=roles_result, ok_handler=lambda roles: (200, [RoleResponseSchema(id=r.role_id, name=r.name) for r in roles]))

    @route.get('/me/can/{action}', auth=JWTAuth(), permissions=None, response={200: CanPermissionResponseSchema})
    def can_current_user(self, request: HttpRequest, action: str):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        can_resp = self.authz_orchestration.can_user(user.id, action)
        return Result.result_parser(result=can_resp, ok_handler=lambda vo: (200, CanPermissionResponseSchema(user_id=vo.user_id, action=vo.action, authorized=vo.authorized)))

    # ---------------- Entitlements / purchases ----------------
    @route.get('/me/entitlements', auth=JWTAuth(), response={200: EntitlementsListResponseSchema})
    def my_entitlements(self, request: HttpRequest):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result = self.authz_orchestration.get_active_entitlements(user.id)
        return Result.result_parser(result=result, ok_handler=lambda e: (200, EntitlementsListResponseSchema(entitlements=e)), default_error_message="failed to fetch entitlements")

    @route.post('/me/restore-purchases', auth=JWTAuth(), response={200: EntitlementsListResponseSchema, 400: ErrorResponseSchema})
    def restore_purchases(self, request: HttpRequest, provider: str, receipt_data: str):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result = self.authz_orchestration.restore_purchases(user.id, provider, receipt_data)
        return Result.result_parser(result=result, ok_handler=lambda ents: (200, EntitlementsListResponseSchema(entitlements=ents)), default_error_message="failed to restore purchases")

    # ---------------- Social / follows ----------------
    @route.get('/me/following', auth=JWTAuth(), response={200: FollowingListResponseSchema})
    def my_following(self, request: HttpRequest):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result = self.user_orchestration.list_following(user.id)
        return Result.result_parser(result=result, ok_handler=lambda fs: (200, FollowingListResponseSchema(following=fs)))

    @route.get('/me/followers', auth=JWTAuth(), response={200: FollowersListResponseSchema})
    def my_followers(self, request: HttpRequest):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result = self.user_orchestration.list_followers(user.id)
        return Result.result_parser(result=result, ok_handler=lambda fs: (200, FollowersListResponseSchema(followers=fs)))

    @route.post('/me/follow/{target_user_id}', auth=JWTAuth(), response={204: None, 400: ErrorResponseSchema})
    def follow_user(self, request: HttpRequest, target_user_id: UUID):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result = self.user_orchestration.follow(user.id, target_user_id)
        return Result.result_parser(result=result, ok_handler=lambda _: (204, None), default_error_message="failed to follow")

    @route.delete('/me/follow/{target_user_id}', auth=JWTAuth(), response={204: None, 400: ErrorResponseSchema})
    def unfollow_user(self, request: HttpRequest, target_user_id: UUID):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result = self.user_orchestration.unfollow(user.id, target_user_id)
        return Result.result_parser(result=result, ok_handler=lambda _: (204, None), default_error_message="failed to unfollow")

    # ---------------- Friend requests ----------------
    @route.post('/me/friend_requests', auth=JWTAuth(), response={201: dict, 400: ErrorResponseSchema})
    def send_friend_request(self, request: HttpRequest, target_user_id: UUID):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result = self.user_orchestration.send_friend_req(user.id, target_user_id)
        return Result.result_parser(result=result, ok_handler=lambda fr: (201, {"id": getattr(fr, "id", None)}), default_error_message="failed to send friend request")

    @route.get('/me/friend_requests', auth=JWTAuth(), response={200: list})
    def list_friend_requests(self, request: HttpRequest, type: str = Query("incoming")):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result = self.user_orchestration.list_friend_reqs(user.id, type)
        return Result.result_parser(result=result, ok_handler=lambda rs: (200, rs), default_error_message="failed to list friend requests")

    @route.put('/me/friend_requests/{request_id}', auth=JWTAuth(), response={200: dict, 400: ErrorResponseSchema})
    def respond_friend_request(self, request: HttpRequest, request_id: UUID, action: str = Query(...)):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result = self.user_orchestration.respond_friend_req(user.id, request_id, action)
        return Result.result_parser(result=result, ok_handler=lambda r: (200, {"status": getattr(r, "status", "ok")}), default_error_message="failed to respond")

    @route.delete('/me/friend_requests/{request_id}', auth=JWTAuth(), response={204: None, 404: ErrorResponseSchema})
    def cancel_friend_request(self, request: HttpRequest, request_id: UUID):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result = self.user_orchestration.cancel_friend_req(user.id, request_id)
        return Result.result_parser(result=result, ok_handler=lambda _: (204, None), default_error_message="failed to cancel")

    # ---------------- Notifications ----------------
    @route.get('/me/notifications', auth=JWTAuth(), response={200: NotificationListResponseSchema})
    def list_notifications(self, request: HttpRequest):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result = self.user_orchestration.list_notifications(user.id)
        return Result.result_parser(result=result, ok_handler=lambda n: (200, NotificationListResponseSchema(notifications=n)), default_error_message="failed to list notifications")

    @route.post('/me/notifications/mark-read', auth=JWTAuth(), response={204: None})
    def mark_notifications_read(self, request: HttpRequest, notification_ids: List[UUID]):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result = self.user_orchestration.mark_notifications_read(user.id, notification_ids)
        return Result.result_parser(result=result, ok_handler=lambda _: (204, None), default_error_message="failed to mark notifications")

    # ---------------- Sessions & Devices ----------------
    @route.get('/me/sessions', auth=JWTAuth(), response={200: SessionsListResponseSchema})
    def list_sessions(self, request: HttpRequest):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result = self.user_orchestration.list_sessions(user.id)
        return Result.result_parser(result=result, ok_handler=lambda s: (200, SessionsListResponseSchema(sessions=s)), default_error_message="failed to list sessions")

    @route.delete('/me/sessions/{session_id}', auth=JWTAuth(), response={204: None})
    def revoke_session(self, request: HttpRequest, session_id: UUID):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result = self.user_orchestration.revoke_session(user.id, session_id)
        return Result.result_parser(result=result, ok_handler=lambda _: (204, None), default_error_message="failed to revoke session")

    @route.get('/me/devices', auth=JWTAuth(), response={200: DevicesListResponseSchema})
    def list_devices(self, request: HttpRequest):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result = self.user_orchestration.list_devices(user.id)
        return Result.result_parser(result=result, ok_handler=lambda d: (200, DevicesListResponseSchema(devices=d)), default_error_message="failed to list devices")

    # ---------------- Account lifecycle ----------------
    @route.post('/me/deactivate', auth=JWTAuth(), response={204: None})
    def deactivate_account(self, request: HttpRequest, reason: str = Query(None)):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result = self.user_orchestration.deactivate_account(user.id, reason)
        return Result.result_parser(result=result, ok_handler=lambda _: (204, None), default_error_message="failed to deactivate account")

    @route.post('/me/delete', auth=JWTAuth(), response={202: dict})
    def request_delete_account(self, request: HttpRequest):
        user = getattr(request, "user", None)
        if not user:
            return 401, ErrorResponseSchema(message="unauthenticated")
        result = self.user_orchestration.request_account_deletion(user.id)
        return Result.result_parser(result=result, ok_handler=lambda payload: (202, payload), default_error_message="failed to request deletion")