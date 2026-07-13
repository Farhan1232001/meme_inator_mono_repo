from uuid import UUID
from typing import Optional, List
from datetime import datetime

from django.http import HttpRequest
from ninja_extra import route

from apps.notifications.application.dtos.notification_schema import NotificationSchema
from apps.notifications.application.dtos.notifications_preferences_schema import NotificationPreferencesSchema
from apps.notifications.application.dtos.success_response_schema import SuccessResponseSchema
from apps.notifications.application.dtos.unread_count_schema import UnreadCountSchema
from apps.notifications.application.orchestration.notifications_orchestration import NotificationsOrchestration
from core.dependency_injections import di
from ninja_jwt.authentication import JWTAuth

from core.dtos.results_schemas import ErrorResponseSchema, NotOkResponseSchema
from core.results import Result


@route.controller("/notifications", tags=["notifications"])
class NotificationsController:
    def __init__(self):
        self._notifications_orchestration: NotificationsOrchestration = (
            di.create_notifications_orchestration()
        )

    # ----------------------------------------------------------------------
    # Notifications
    # ----------------------------------------------------------------------
    @route.get(
        "/",
        tags=["notifications"],
        permissions=None,
        auth=JWTAuth(),
        response={
            200: List[NotificationSchema],
            401: NotOkResponseSchema,
            500: ErrorResponseSchema,
        },
        description="Get the authenticated user's notifications with pagination.",
    )
    def get_notifications(
        self,
        request: HttpRequest,
        page_size: Optional[int] = 10, # number of notifications per page. 
        cursor: Optional[str] = None,
        unread_only: bool = False,
    ):
        """Retrieve notifications for the authenticated user."""
        user_id = request.user.id

        result = self._notifications_orchestration.list_notifications(
            user_id=user_id, page_size=page_size, cursor=cursor, unread_only=unread_only
        )

        return Result.result_parser(
            result=result,
            ok_handler=lambda value: (200, value),
            default_error_message="Internal server error",
        )

    @route.delete(
        "/",
        tags=["notifications"],
        permissions=None,
        auth=JWTAuth(),
        response={
            204: None,  # No content
            401: NotOkResponseSchema,
            500: ErrorResponseSchema,
        },
        description="Clear all notifications for the authenticated user.",
    )
    def clear_all_notifications(self, request: HttpRequest):
        """Delete all notifications of the authenticated user."""
        user_id = request.user.id

        result = self._notifications_orchestration.clear_all_notifications(user_id)

        return Result.result_parser(
            result=result,
            ok_handler=lambda _: (204, None),
            default_error_message="Internal server error",
        )

    @route.put(
        "/{notification_id}/read",
        tags=["notifications"],
        permissions=None,
        auth=JWTAuth(),
        response={
            200: NotificationSchema,
            404: NotOkResponseSchema,
            500: ErrorResponseSchema,
        },
        description="Mark a single notification as read.",
    )
    def mark_notification_as_read(
        self, request: HttpRequest, notification_id: UUID
    ):
        """Mark a specific notification as read."""
        user_id = request.user.id

        result = self._notifications_orchestration.mark_as_read(
            user_id=user_id, notification_id=notification_id
        )

        return Result.result_parser(
            result=result,
            ok_handler=lambda value: (200, value),
            default_error_message="Internal server error",
        )

    @route.put(
        "/read/all",
        tags=["notifications"],
        permissions=None,
        auth=JWTAuth(),
        response={
            200: SuccessResponseSchema,  # e.g., {"marked_count": 5}
            500: ErrorResponseSchema,
        },
        description="Mark all notifications as read for the authenticated user.",
    )
    def mark_all_as_read(self, request: HttpRequest):
        """Mark every notification of the user as read."""
        user_id = request.user.id

        result = self._notifications_orchestration.mark_all_as_read(user_id)

        return Result.result_parser(
            result=result,
            ok_handler=lambda count: (200, {"marked_count": count}),
            default_error_message="Internal server error",
        )

    @route.get(
        "/unread/count",
        tags=["notifications"],
        permissions=None,
        auth=JWTAuth(),
        response={
            200: UnreadCountSchema,
            401: NotOkResponseSchema,
            500: ErrorResponseSchema,
        },
        description="Get the number of unread notifications.",
    )
    def get_unread_count(self, request: HttpRequest):
        """Return the unread notification count for the user."""
        user_id = request.user.id

        result = self._notifications_orchestration.get_unread_count(user_id)

        return Result.result_parser(
            result=result,
            ok_handler=lambda count: (200, {"unread_count": count}),
            default_error_message="Internal server error",
        )

    # ----------------------------------------------------------------------
    # Notification Preferences
    # ----------------------------------------------------------------------
    @route.get(
        "/preferences",
        tags=["notifications"],
        permissions=None,
        auth=JWTAuth(),
        response={
            200: NotificationPreferencesSchema,
            404: NotOkResponseSchema,
            500: ErrorResponseSchema,
        },
        description="Get the notification preferences for the authenticated user.",
    )
    def get_preferences(self, request: HttpRequest):
        """Retrieve the user's notification preferences."""
        user_id = request.user.id

        result = self._notifications_orchestration.get_preferences(user_id)

        return Result.result_parser(
            result=result,
            ok_handler=lambda value: (200, value),
            default_error_message="Internal server error",
        )

    @route.patch(
        "/preferences",
        tags=["notifications"],
        permissions=None,
        auth=JWTAuth(),
        response={
            200: NotificationPreferencesSchema,
            400: NotOkResponseSchema,
            404: NotOkResponseSchema,
            500: ErrorResponseSchema,
        },
        description="Partially update the user's notification preferences.",
    )
    def patch_preferences(self, request: HttpRequest, payload: dict):
        """Update notification preferences (e.g., enable/disable channels, mute types, set digest)."""
        user_id = request.user.id

        result = self._notifications_orchestration.update_preferences(
            user_id=user_id, updates=payload
        )

        return Result.result_parser(
            result=result,
            ok_handler=lambda value: (200, value),
            default_error_message="Internal server error",
        )

    # Optional: Replace preferences entirely (PUT) – similar to ProfilesController
    @route.put(
        "/preferences",
        tags=["notifications"],
        permissions=None,
        auth=JWTAuth(),
        response={
            200: NotificationPreferencesSchema,
            400: NotOkResponseSchema,
            404: NotOkResponseSchema,
            500: ErrorResponseSchema,
        },
        description="Fully replace the user's notification preferences.",
    )
    def replace_preferences(self, request: HttpRequest, payload: dict):
        """Replace all notification preferences with the provided object."""
        user_id = request.user.id

        # The orchestration method can be the same as update_preferences,
        # but with a flag for full replacement, or use a separate method.
        result = self._notifications_orchestration.replace_preferences(
            user_id=user_id, preferences=payload
        )

        return Result.result_parser(
            result=result,
            ok_handler=lambda value: (200, value),
            default_error_message="Internal server error",
        )

