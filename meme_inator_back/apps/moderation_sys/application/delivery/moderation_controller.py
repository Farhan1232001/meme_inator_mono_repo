# application/controllers/moderation_controller.py
from django.http import HttpRequest
from ninja import Body, File, Form, UploadedFile
from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth
from typing import Optional
from uuid import UUID
from apps.moderation_sys.application.orchestration.moderation_orchestration import ModerationOrchestration
from apps.moderation_sys.application.schemas.moderation_submission_request import ModerationSubmissionRequestSchema
from apps.moderation_sys.application.schemas.request_schemas import HumanModerationRequestSchema, ResolveAppealRequestSchema, SubmitAppealRequestSchema
from apps.moderation_sys.application.schemas.response_schemas import AppealResponseSchema, ModerationCaseResponseSchema
from apps.moderation_sys.domain.aggregates.moderation_case import ModerationCase
from core.dependency_injections import di
from core.dtos.results_schemas import ErrorResponseSchema, NotOkResponseSchema
from core.results import Result
import json

@api_controller("/moderation", tags=["moderation"])
class ModerationController:
    def __init__(self):
        self._orchestrator: ModerationOrchestration = di.create_moderation_orchestration()

    @route.post(
        "/submit",
        auth=JWTAuth(),
        response={
            201: ModerationCaseResponseSchema,
            400: NotOkResponseSchema,
            500: ErrorResponseSchema
        }
    )
    def submit_content_for_moderation(
        self, 
        body: ModerationSubmissionRequestSchema,
        image: UploadedFile = File(None),
        video: UploadedFile = File(None)
    ):
        """Submit user content for moderation."""

        submission_data = body.model_dump()

        # Attach uploaded image bytes
        if image:
            submission_data["image_content"]["image_data"] = image.read()

        # Attach uploaded video bytes
        if video:
            submission_data["video_content"]["video_data"] = video.read()

        # Re-validate after mutation
        submission = ModerationSubmissionRequestSchema(**submission_data)
            
        # 3. Submit and return result
        result:Result[ModerationCase] = self._orchestrator.submit_moderation_case(submission)
        return Result.result_parser(
            result=result,
            ok_handler=lambda value: (201, value),
            default_error_message="Failed to submit content for moderation"
        )

    @route.post(
        "/human/moderate",
        auth=JWTAuth(),
        response={
            200: ModerationCaseResponseSchema,
            400: NotOkResponseSchema,
            500: ErrorResponseSchema
        }
    )
    def human_moderate_content(self, request: HttpRequest, payload: HumanModerationRequestSchema):
        """Human moderator reviews and decides on content."""
        moderator_id = request.user.id
        result = self._orchestrator.human_moderate(payload, moderator_id)
        return Result.result_parser(
            result=result,
            ok_handler=lambda value: (200, value),
            default_error_message="Failed to process human moderation"
        )

    @route.post(
        "/appeal",
        auth=JWTAuth(),
        response={
            201: AppealResponseSchema,
            400: NotOkResponseSchema,
            500: ErrorResponseSchema
        }
    )
    def submit_appeal(self, request: HttpRequest, payload: SubmitAppealRequestSchema):
        """Submit an appeal for a rejected moderation decision."""
        user_id = request.user.id
        result = self._orchestrator.submit_appeal(payload, user_id)
        return Result.result_parser(
            result=result,
            ok_handler=lambda value: (201, value),
            default_error_message="Failed to submit appeal"
        )

    @route.post(
        "/appeal/resolve",
        auth=JWTAuth(),
        response={
            200: ModerationCaseResponseSchema,
            400: NotOkResponseSchema,
            500: ErrorResponseSchema
        }
    )
    def resolve_appeal(self, request: HttpRequest, payload: ResolveAppealRequestSchema):
        """Moderator resolves an appeal."""
        moderator_id = request.user.id
        result = self._orchestrator.resolve_appeal(payload, moderator_id)
        return Result.result_parser(
            result=result,
            ok_handler=lambda value: (200, value),
            default_error_message="Failed to resolve appeal"
        )