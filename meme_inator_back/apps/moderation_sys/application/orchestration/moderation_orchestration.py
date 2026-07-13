# apps/moderation_sys/application/orchestration/moderation_orchestration.py

from uuid import UUID
from typing import Optional
import logging
from apps.moderation_sys.application.schemas.moderation_submission_request import ModerationSubmissionRequestSchema, TextContentSchema
from apps.moderation_sys.application.schemas.request_schemas import (
    ResolveAppealRequestSchema,
    SubmitAppealRequestSchema,
    HumanModerationRequestSchema,
    UpdatePolicyRequestSchema,
)
from apps.moderation_sys.application.usecases.submit_moderation_case import SubmitModerationCaseUsecase
from apps.moderation_sys.application.usecases.process_content_for_moderation import ProcessContentForModerationUsecase
from apps.moderation_sys.application.usecases.direct_for_human_moderation import DirectContentForHumanModerationUsecase
from apps.moderation_sys.application.usecases.submit_appeal import SubmitAppealUsecase
from apps.moderation_sys.application.usecases.resolve_appeal import ResolveAppealUsecase
from apps.moderation_sys.application.usecases.notify_user_of_moderated_content import NotifyUserOfModeratedContentUsecase
from apps.moderation_sys.application.usecases.run_moderation_drift_cron import RunModerationDriftCronJobUsecase
from apps.moderation_sys.application.usecases.switch_to_fallback_provider import SwitchToFallbackProviderUsecase
from apps.moderation_sys.application.usecases.update_policy import UpdatePolicyUsecase
from apps.moderation_sys.domain.aggregates.moderation_case import ModerationCase
from apps.moderation_sys.domain.enums.media_src_enum import MediaSourceEnum
from apps.moderation_sys.domain.enums.media_type_enums import MediaTypeEnum
from apps.moderation_sys.domain.value_objects.content_to_mod.atomic_vos.img_to_mod import ImageToModerateVo
from apps.moderation_sys.domain.value_objects.content_to_mod.atomic_vos.txt_to_mod import TextToModerateVo
from apps.moderation_sys.domain.value_objects.content_to_mod.atomic_vos.video_to_mod import VideoToModerateVo
from apps.moderation_sys.domain.value_objects.content_to_mod.content_to_moderate import ContentToModerateVo
from core.results import Result

logger = logging.getLogger(__name__)


class ModerationOrchestration:
    """
    Orchestrates moderation flows by delegating to injected use cases.
    All dependencies (repositories, services, use cases) are provided at construction.
    """

    def __init__(
        self,
        submit_moderation_usecase: SubmitModerationCaseUsecase,
        process_content_usecase: ProcessContentForModerationUsecase,
        direct_human_moderation_usecase: DirectContentForHumanModerationUsecase,
        submit_appeal_usecase: SubmitAppealUsecase,
        resolve_appeal_usecase: ResolveAppealUsecase,
        notify_user_usecase: NotifyUserOfModeratedContentUsecase,
        run_drift_cron_usecase: RunModerationDriftCronJobUsecase,
        switch_provider_usecase: SwitchToFallbackProviderUsecase,
        update_policy_usecase: UpdatePolicyUsecase,
    ):
        self.submit_moderation_usecase = submit_moderation_usecase
        self.process_content_usecase = process_content_usecase
        self.direct_human_moderation_usecase = direct_human_moderation_usecase
        self.submit_appeal_usecase = submit_appeal_usecase
        self.resolve_appeal_usecase = resolve_appeal_usecase
        self.notify_user_usecase = notify_user_usecase
        self.run_drift_cron_usecase = run_drift_cron_usecase
        self.switch_provider_usecase = switch_provider_usecase
        self.update_policy_usecase = update_policy_usecase

    # -------------------------------------------------------------------------
    # Public orchestration methods – each simply delegates to the corresponding use case
    # -------------------------------------------------------------------------

    def submit_moderation_case(self, submission: ModerationSubmissionRequestSchema) -> Result[ModerationCase]:
        content:ContentToModerateVo = self._build_content_vo(submission)
        return self.submit_moderation_usecase.execute(content)

    def process_content(self, case_id: Optional[UUID], case: Optional[ModerationCase]) -> Result:
        return self.process_content_usecase.execute(
            case_id=case_id,
            case=case
        )

    def ingest_and_process_content(self, submission: ModerationSubmissionRequestSchema) -> Result[ModerationCase]:
        """Complete upstream flow: ingest → process (no downstream stages)."""
        # 1. Ingest/Submit (upstream)
        content_vo = self._build_content_vo(submission)
        case_result = self.submit_moderation_usecase.execute(content_vo)
        
        if case_result.is_error:
            return case_result
        
        # 2. Process immediately (not waiting for cron/batch)
        case = case_result.value
        process_result = self.process_content_usecase.execute(case.id)
        
        if process_result.is_error:
            # Log but return case - partial completion
            logger.warning(f"Processing failed after ingestion for {case.id}")
        
        return case_result  # Return the case (may be pending processing)

    def human_moderate(self, request: HumanModerationRequestSchema, moderator_id: UUID) -> Result:
        return self.direct_human_moderation_usecase.execute(
            case_id=request.case_id,
            decision=request.decision,
            moderator_id=moderator_id,
            note=request.note,
        )

    def submit_appeal(self, request: SubmitAppealRequestSchema, user_id: UUID) -> Result:
        return self.submit_appeal_usecase.execute(
            case_id=request.case_id,
            user_id=user_id,
            reason=request.reason,
        )

    def resolve_appeal(self, request: ResolveAppealRequestSchema, moderator_id: UUID) -> Result:
        return self.resolve_appeal_usecase.execute(
            case_id=request.case_id,
            outcome=request.outcome,
            moderator_id=moderator_id,
            resolution_note=request.resolution_note,
        )

    def notify_user(self, case_id: UUID) -> Result:
        return self.notify_user_usecase.execute(case_id)

    def run_drift_detection(self, lookback_hours: int = 24) -> Result:
        return self.run_drift_cron_usecase.execute(lookback_hours)

    def switch_to_fallback_provider(self, primary_provider: str) -> Result:
        return self.switch_provider_usecase.execute(primary_provider)

    def update_policy(self, request: UpdatePolicyRequestSchema, admin_id: UUID) -> Result:
        return self.update_policy_usecase.execute(
            policy_id=request.policy_id,
            admin_id=admin_id,
            updates=request.dict(exclude_unset=True),
        )


    def _build_content_vo(self, submission: ModerationSubmissionRequestSchema) -> ContentToModerateVo:
        """Build ContentToModerateVo from the Ninja submission schema."""
        media_type = MediaTypeEnum(submission.content_type)
        media_src = MediaSourceEnum(submission.content_source)
        
        # Only one of these attributes can be non-null
        text_content = None
        image_content = None
        video_content = None
        
        if media_type == MediaTypeEnum.TEXT:
            text_content = TextToModerateVo(
                text=submission.text_content.text or "",
                language=submission.text_content.language  # Could be extracted if available
            )
        elif media_type == MediaTypeEnum.IMG:
            img = submission.image_content
            image_content = ImageToModerateVo(
                image_data=img.image_data,
                image_url=img.image_url,
                retrieval_key=img.retrieval_key if media_src != MediaSourceEnum.REQUEST_BODY else None,
                format=None  # Could be inferred from URL
            )
        elif media_type == MediaTypeEnum.VIDEO:
            video = submission.video_content
            video_content = VideoToModerateVo(
                video_data=video.video_data,
                video_url=video.video_url,
                retrieval_key=video.retrieval_key if media_src != MediaSourceEnum.REQUEST_BODY else None,
                format=None
            )
        
        return ContentToModerateVo(
            content_id=submission.content_id,
            author_id=submission.author_id,
            policy_routing_key=submission.policy_routing_key,
            content_type=media_type,
            content_src=media_src,
            region=submission.region,
            text_content=text_content,
            image_content=image_content,
            video_content=video_content
        )