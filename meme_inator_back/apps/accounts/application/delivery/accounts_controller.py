# apps/accounts/api/controllers/accounts_controller.py
from ninja_extra import api_controller, ControllerBase, route
from ninja_extra.permissions import AllowAny
from ninja import Request
from ninja_jwt.authentication import JWTAuth

from apps.accounts.application.dtos.accounts_schemas import (
    PasswordChangeRequestSchema,
    PasswordChangeResponseSchema,
    PasswordResetIntentRequestSchema,
    PasswordResetIntentResponseSchema,
    PasswordResetConfirmRequestSchema,
    PasswordResetConfirmResponseSchema,
    EmailChangeIntentRequestSchema,
    EmailChangeIntentResponseSchema,
    EmailChangeConfirmRequestSchema,
    EmailChangeConfirmResponseSchema,
)
from core.dtos.results_schemas import ErrorResponseSchema, NotOkResponseSchema
from core.results import Ok, NotOk, Error, Result
from core.dependency_injections import di
from meme_inator_back import settings


@api_controller(
    "/accounts",
    tags=["accounts"],
    permissions=[AllowAny],
)
class AccountsController(ControllerBase):
    """
    Accounts-related endpoints (password management, email change).
    Uses constructor-based DI and maps Result -> HTTP responses via match.
    """

    def __init__(self):
        super().__init__()
        self._password_orchestration = di.create_user_password_orchestration()


    # -----------------------------
    # Change password (authenticated)
    # -----------------------------
    @route.post(
        "/password/change",
        response={
            200: PasswordChangeResponseSchema,
            400: NotOkResponseSchema,
            401: NotOkResponseSchema,
            500: ErrorResponseSchema,
        },
        auth=JWTAuth(),
    )
    def change_password(self, request: Request, payload: PasswordChangeRequestSchema):
        user_id = self._extract_user_id(request)
        if not user_id:
            return 401, NotOkResponseSchema(message="authentication required")

        result = self._password_orchestration.change_password(
            user_id=user_id,
            current_password=payload.current_password,
            new_password=payload.new_password,
        )

        return self._map_result(
            result,
            ok_response=(200, PasswordChangeResponseSchema(
                success=True,
                message="Password updated",
            )),
        )

    # -----------------------------
    # Password reset: intent (send)
    # -----------------------------
    @route.post(
        "/password/reset/intent",
        response={
            201: PasswordResetIntentResponseSchema,
            400: NotOkResponseSchema,
            500: ErrorResponseSchema,
        },
    )
    def password_reset_intent(self, request: Request, payload: PasswordResetIntentRequestSchema):
        result = self._password_orchestration.reset_password_intent(
            email=payload.email
        )

        return self._map_result(
            result,
            ok_response=(201, PasswordResetIntentResponseSchema(
                success=True,
                message="Reset challenge sent",
            )),
        )

    # -----------------------------
    # Password reset: confirm (complete)
    # -----------------------------
    @route.post(
        "/password/reset/confirm",
        response={
            200: PasswordResetConfirmResponseSchema,
            400: NotOkResponseSchema,
            401: NotOkResponseSchema,
            410: NotOkResponseSchema,
            500: ErrorResponseSchema,
        },
    )
    def password_reset_confirm(self, request: Request, payload: PasswordResetConfirmRequestSchema):
        result = self._password_orchestration.reset_password_confirm(
            challenge_code=payload.challenge_code,
            new_password=payload.new_password,
        )

        return self._map_result(
            result,
            ok_response=(200, PasswordResetConfirmResponseSchema(
                success=True,
                message="Password reset successful",
            )),
        )

    # -----------------------------
    # Email change: intent (send)
    # -----------------------------
    @route.post(
        "/email/change/intent",
        response={
            201: EmailChangeIntentResponseSchema,
            400: NotOkResponseSchema,
            401: NotOkResponseSchema,
            500: ErrorResponseSchema,
        },
        auth=JWTAuth(),
    )
    def email_change_intent(self, request: Request, payload: EmailChangeIntentRequestSchema):
        raise NotImplementedError("email_change_intent is not implemented")

    # -----------------------------
    # Email change: confirm (complete)
    # -----------------------------
    @route.post(
        "/email/change/confirm",
        response={
            200: EmailChangeConfirmResponseSchema,
            400: NotOkResponseSchema,
            401: NotOkResponseSchema,
            410: NotOkResponseSchema,
            500: ErrorResponseSchema,
        },
        auth=JWTAuth(),
    )
    def email_change_confirm(self, request: Request, payload: EmailChangeConfirmRequestSchema):
        raise NotImplementedError("email_change_confirm is not implemented")

    # ------------------------------------------------
    # Helpers
    # ------------------------------------------------
    def _map_result(self, result: Result, *, ok_response):
        """
        Centralized Result -> HTTP mapping.
        """
        match result:
            case Ok():
                return ok_response

            case NotOk(message=msg, static_msg=static, status_code=code):
                return code, NotOkResponseSchema(
                    message=msg,
                    static_msg=static,
                )

            case Error(message=msg, exception=exc, status_code=code):
                if settings.DEBUG:
                    return code, ErrorResponseSchema(
                        message=msg,
                        static_msg=None,
                        exception_str=str(exc),
                    )
                return code, ErrorResponseSchema(message="internal server error")

            case _:
                return 500, ErrorResponseSchema(message="unexpected result")

    def _extract_user_id(self, request: Request):
        """
        Extract user_id from request.user or request.auth.
        """
        try:
            user = getattr(request, "user", None)
            if user and getattr(user, "id", None):
                return user.id

            auth = getattr(request, "auth", None)
            if isinstance(auth, dict):
                return auth.get("user_id")
        except Exception:
            pass

        return None
