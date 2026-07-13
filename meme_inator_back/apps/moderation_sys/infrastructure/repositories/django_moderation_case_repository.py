from datetime import datetime, timezone
from uuid import UUID
from typing import Optional, List
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from apps.moderation_sys.domain.aggregates.moderation_case import ModerationCase
from apps.moderation_sys.domain.entities.appeal_entity import AppealEntity
from apps.moderation_sys.domain.entities.moderation_attempt_entity import ModerationAttemptEntity
from apps.moderation_sys.domain.enums.media_src_enum import MediaSourceEnum
from apps.moderation_sys.domain.enums.media_type_enums import MediaTypeEnum
from apps.moderation_sys.domain.enums.moderation_enums import AppealStatusEnum, CaseStatusEnum, DecisionEnum, ModerationActionEnum, ModerationProviderEnum, VisibilityEffectEnum
from apps.moderation_sys.domain.irepositories.moderation_case_repository import IModerationCaseRepository
from apps.moderation_sys.domain.irepositories.blob_storage_repository import IBlobStorageRepository
from apps.moderation_sys.domain.value_objects.confidence_score import ConfidenceScoreVo
from apps.moderation_sys.domain.value_objects.content_fingerprint import ContentFingerprintVo
from apps.moderation_sys.domain.value_objects.content_snapshot_vo import ContentSnapshotVo, ImageSnapshotVo, TextSnapshotVo, VideoSnapshotVo
from apps.moderation_sys.domain.value_objects.content_to_mod.content_to_moderate import ContentToModerateVo, ImageToModerateVo, TextToModerateVo, VideoToModerateVo
from apps.moderation_sys.domain.value_objects.moderation_action import ModerationActionVo
from apps.moderation_sys.domain.value_objects.moderation_decision import ModerationDecisionVo
from apps.moderation_sys.infrastructure.models.content_blob_model import ContentBlobModel
from apps.moderation_sys.infrastructure.models.content_snapshot_model import ContentSnapshotModel
from apps.moderation_sys.infrastructure.models.fingerprint_model import FingerprintModel
from apps.moderation_sys.infrastructure.models.moderation_action_model import ModerationActionModel
from apps.moderation_sys.infrastructure.models.moderation_appeal_model import ModerationAppealModel
from apps.moderation_sys.infrastructure.models.moderation_attempt_model import ModerationAttemptModel
from apps.moderation_sys.infrastructure.models.moderation_case_model import ModerationCaseModel
from apps.moderation_sys.infrastructure.models.moderation_decision_model import ModerationDecisionModel
from core.results import NotOk, Ok, Result
from django.contrib.auth import get_user_model

User = get_user_model()


class DjangoModerationCaseRepository(IModerationCaseRepository):
    """Django implementation of ModerationCaseRepository using blob storage repository."""

    # TODO: Is injecting repo inside another repo bad design?
    def __init__(self, blob_storage_repo: IBlobStorageRepository):
        self.blob_storage_repo = blob_storage_repo

    @transaction.atomic
    def save(self, case: ModerationCase) -> Result[ModerationCase]:
        # ---------------------------------------------------------------
        # 1. Store or retrieve ContentBlob using blob storage repository
        # ---------------------------------------------------------------
        content_vo = case.content
        raw_bytes = self._extract_raw_bytes(content_vo)
        blob_ref = self.blob_storage_repo.store(content_vo, raw_bytes)
        
        # Get the actual ContentBlobModel instance for FK relationships
        blob_model = ContentBlobModel.objects.get(id=blob_ref.blob_id)

        # ---------------------------------------------------------------
        # 2. Action, Decision, Fingerprint (ContentToModerateModel REMOVED)
        # ---------------------------------------------------------------
        action_model = None
        if case.action:
            action_model, _ = ModerationActionModel.objects.update_or_create(
                action_type=case.action.action_type.value,
                visibility_effect=case.action.visibility_effect.value,
                reason=case.action.reason,
            )

        decision_model = None
        if case.decision:
            decision_model, _ = ModerationDecisionModel.objects.update_or_create(
                outcome=case.decision.outcome.value,
                reason_code=case.decision.reason_code or '',
                note=case.decision.note or '',
            )

        fingerprint_model = None
        if case.content_fingerprint:
            fp = case.content_fingerprint
            fingerprint_model, _ = FingerprintModel.objects.get_or_create(
                fingerprint_hash=fp.fingerprint_hash,
                defaults={
                    'content_type': fp.content_type,
                    'policy_routing_key': fp.policy_routing_key,
                    'provider_used': fp.provider_used.value,
                    'decision_outcome': fp.decision_outcome.value,
                    'confidence_score': fp.confidence_score,
                    'created_at': fp.created_at,
                    'expires_at': fp.expires_at,
                }
            )

        # ---------------------------------------------------------------
        # 3. Main Case Model
        # ---------------------------------------------------------------
        case_model = ModerationCaseModel.objects.filter(case_id=case.case_id).first()

        if case_model is None:
            # CREATE path
            try:
                user = User.objects.get(id=case.user_id)
            except User.DoesNotExist:
                return NotOk(message="error : User not found", status_code=404)

            # Extract loose-reference from content_vo
            # The content_id is now a reference to the external entity (e.g., PostModel)
            source_app = content_vo.content_src.value  # or derive from routing_key
            source_model_type = content_vo.content_type.value  # "comment", "image", "video"
            source_model_id = content_vo.content_id  # This is the UUID of the external entity

            case_model = ModerationCaseModel.objects.create(
                case_id=case.case_id,
                user=user,
                source_app=source_app,
                source_model_type=source_model_type,
                source_model_id=source_model_id,
                policy_routing_key=case.policy_routing_key,
                content_type=case.content_type,
                region=case.region,
                status=case.status,
                action=action_model,
                decision=decision_model,
                confidence_score=case.confidence_score.value if case.confidence_score else None,
                provider_used=case.provider_used.value if case.provider_used else None,
                created_at=case.created_at,
                decided_at=case.decided_at,
            )
            
            # Save snapshot after case exists
            if case.content_snapshot:
                snapshot_model = self._save_snapshot(case, case_model, blob_model)
                snapshot_model.mod_case = case_model
                snapshot_model.save()
                
                # Update fingerprint with case reference if needed
                if fingerprint_model:
                    fingerprint_model.case = case_model
                    fingerprint_model.save(update_fields=['case'])
            
            # Save appeal after case exists
            if case.appeal:
                appeal_model = self._save_appeal(case_model, case.appeal)
                case_model.appeal = appeal_model
                case_model.save(update_fields=['appeal'])
                
        else:
            # UPDATE path
            case_model.status = case.status
            case_model.action = action_model
            case_model.decision = decision_model
            case_model.confidence_score = case.confidence_score.value if case.confidence_score else None
            case_model.provider_used = case.provider_used.value if case.provider_used else None
            case_model.decided_at = case.decided_at

            if case.appeal:
                case_model.appeal = self._save_appeal(case_model, case.appeal)

            case_model.save(update_fields=[
                'status', 'action', 'decision', 'confidence_score',
                'provider_used', 'decided_at', 'appeal',
            ])

        saved_model = case_model if case_model else ModerationCaseModel.objects.get(case_id=case.case_id)
        domain_case = self._to_domain(saved_model)
        return Ok(domain_case)

    def _extract_raw_bytes(self, content_vo: ContentToModerateVo) -> Optional[bytes]:
        """Extract raw bytes from content_vo if available (REQUEST_BODY case)."""
        if content_vo.content_src != MediaSourceEnum.REQUEST_BODY:
            return None
        if content_vo.text_content:
            return content_vo.text_content.text.encode('utf-8')
        if content_vo.image_content:
            return content_vo.image_content.image_data
        if content_vo.video_content:
            return content_vo.video_content.video_data
        return None

    def _save_snapshot(self, case: ModerationCase, case_model: ModerationCaseModel, blob_model: ContentBlobModel) -> ContentSnapshotModel:
        """Create the immutable snapshot for the case."""
        snapshot_vo = case.content_snapshot
        if snapshot_vo is None:
            raise ValueError("Snapshot is required for case creation")

        snapshot_model, created = ContentSnapshotModel.objects.get_or_create(
            snapshot_id=snapshot_vo.id,
            defaults={
                'mod_case': case_model,  # Set it directly in creation
                'content_blob': blob_model,
                'captured_at': snapshot_vo.captured_at or datetime.now(timezone.utc),
            }
        )
        
        # If it already existed but without mod_case (shouldn't happen), update it
        if not created and snapshot_model.mod_case is None:
            snapshot_model.mod_case = case_model
            snapshot_model.save()
            
        return snapshot_model

    def _save_appeal(
        self,
        case_model: ModerationCaseModel,
        appeal: Optional[AppealEntity]
    ) -> Optional[ModerationAppealModel]:
        """Save appeal entity."""
        if appeal is None:
            return None

        appeal_model = ModerationAppealModel.objects.filter(
            appeal_id=appeal.appeal_id
        ).first()

        if appeal_model is None:
            appeal_model = ModerationAppealModel.objects.create(
                appeal_id=appeal.appeal_id,
                case=case_model,
                submitted_by=appeal.submitted_by,
                reason=appeal.reason,
                submitted_at=appeal.submitted_at,
                status=appeal.status.value,
            )
        else:
            appeal_model.reason = appeal.reason
            appeal_model.status = appeal.status.value
            appeal_model.save(update_fields=["reason", "status"])

        return appeal_model

    def _save_attempt(
        self,
        case_model: ModerationCaseModel,
        attempt: ModerationAttemptEntity
    ) -> ModerationAttemptModel:
        """Save moderation attempt entity."""
        attempt_model = ModerationAttemptModel.objects.filter(
            attempt_id=attempt.attempt_id
        ).first()

        if attempt_model is None:
            attempt_model = ModerationAttemptModel.objects.create(
                attempt_id=attempt.attempt_id,
                case=case_model,
                moderator_id=attempt.moderator_id,
                decision=attempt.decision,
                note=attempt.note,
                attempted_at=attempt.attempted_at,
                resolved_at=attempt.resolved_at,
                resolution_note=attempt.resolution_note,
            )
        else:
            attempt_model.moderator_id = attempt.moderator_id
            attempt_model.decision = attempt.decision
            attempt_model.note = attempt.note
            attempt_model.resolved_at = attempt.resolved_at
            attempt_model.resolution_note = attempt.resolution_note
            attempt_model.save(update_fields=[
                "moderator_id", "decision", "note", "resolved_at", "resolution_note"
            ])

        return attempt_model

    def find_by_id(self, case_id: UUID) -> Optional[ModerationCase]:
        try:
            model = ModerationCaseModel.objects \
                .select_related('action', 'decision', 'appeal') \
                .prefetch_related('attempts') \
                .get(case_id=case_id)
            return self._to_domain(model)
        except ModerationCaseModel.DoesNotExist:
            return None

    def find_pending_by_content_id(self, content_id: UUID) -> Optional[ModerationCase]:
        try:
            model = ModerationCaseModel.objects \
                .select_related('action', 'decision', 'appeal') \
                .prefetch_related('attempts') \
                .filter(
                    source_model_id=content_id,  # Now using loose reference
                    status__in=[CaseStatusEnum.PENDING.value, CaseStatusEnum.FLAGGED.value]
                ) \
                .latest('created_at')
            return self._to_domain(model)
        except ModerationCaseModel.DoesNotExist:
            return None


    def find_by_status(self, status: str, limit: int = 100) -> List[ModerationCase]:
        """Find cases by status."""
        models = ModerationCaseModel.objects \
            .select_related('content_id', 'content_snapshot', 'content_fingerprint',
                           'action', 'decision', 'appeal') \
            .prefetch_related('attempts') \
            .filter(status=status) \
            .order_by('-created_at')[:limit]
        return [self._to_domain(model) for model in models]

    def find_by_author_id(self, author_id: UUID, limit: int = 50) -> List[ModerationCase]:
        """Find cases by author ID."""
        models = ModerationCaseModel.objects \
            .select_related('content_id', 'content_snapshot', 'content_fingerprint',
                           'action', 'decision', 'appeal') \
            .prefetch_related('attempts') \
            .filter(user_id=author_id) \
            .order_by('-created_at')[:limit]
        return [self._to_domain(model) for model in models]

    def find_appeals_pending_review(self, limit: int = 100) -> List[ModerationCase]:
        """Find cases with pending appeals."""
        models = ModerationCaseModel.objects \
            .select_related('content_id', 'content_snapshot', 'content_fingerprint',
                           'action', 'decision', 'appeal') \
            .prefetch_related('attempts') \
            .filter(
                appeal__status=AppealStatusEnum.PENDING.value,
                status=CaseStatusEnum.APPEALING.value
            ) \
            .order_by('appeal__submitted_at')[:limit]
        return [self._to_domain(model) for model in models]

    def find_flagged_for_human_review(self, limit: int = 100) -> List[ModerationCase]:
        """Find cases flagged for human review."""
        models = ModerationCaseModel.objects \
            .select_related('content_id', 'content_snapshot', 'content_fingerprint',
                           'action', 'decision', 'appeal') \
            .prefetch_related('attempts') \
            .filter(status=CaseStatusEnum.FLAGGED.value) \
            .order_by('created_at')[:limit]
        return [self._to_domain(model) for model in models]

    def find_by_provider_and_fingerprint(
        self, 
        provider: ModerationProviderEnum, 
        fingerprint_hash: str
    ) -> Optional[ModerationCase]:
        """Find cases by provider and fingerprint hash for drift detection."""
        try:
            model = ModerationCaseModel.objects \
                .select_related('content_id', 'content_snapshot', 'content_fingerprint',
                               'action', 'decision', 'appeal') \
                .prefetch_related('attempts') \
                .filter(
                    provider_used=provider.value,
                    content_fingerprint__fingerprint_hash=fingerprint_hash
                ) \
                .latest('created_at')
            return self._to_domain(model)
        except ModerationCaseModel.DoesNotExist:
            return None
        
    def exists_pending_for_content(self, content_id: UUID) -> bool:
        return ModerationCaseModel.objects.filter(
            source_model_id=content_id,
            source_model_type="comment",  # or whatever type
            status__in=[CaseStatusEnum.PENDING.value, CaseStatusEnum.FLAGGED.value]
        ).exists()
    
    def count_appeals_by_user_today(self, user_id: UUID) -> int:
        """Count appeals submitted by user today."""
        from django.utils import timezone
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return ModerationAppealModel.objects.filter(
            submitted_by=user_id,
            submitted_at__gte=today_start
        ).count()

    @transaction.atomic
    def delete(self, case_id: UUID) -> bool:
        """Delete a moderation case."""
        try:
            model = ModerationCaseModel.objects.get(case_id=case_id)
            model.delete()
            return True
        except ModerationCaseModel.DoesNotExist:
            return False

    def _to_domain(self, model: ModerationCaseModel) -> ModerationCase:
        """Convert Django model to domain aggregate root."""

        # 1. Reconstruct ContentToModerateVo from loose reference fields
        content_type = MediaTypeEnum(model.content_type)
        
        # You'll need to get text/image/video VOs from somewhere
        # For now, creating minimal VOs with None for heavy data
        text_vo = image_vo = video_vo = None
        
        if content_type == MediaTypeEnum.TEXT:
            # Text content would need to be fetched from the source entity
            text_vo = TextToModerateVo(text="", language=None)
        elif content_type == MediaTypeEnum.IMG:
            image_vo = ImageToModerateVo(
                image_data=None,
                image_url=None,
                retrieval_key=None,
                format=None,
            )
        elif content_type == MediaTypeEnum.VIDEO:
            video_vo = VideoToModerateVo(
                video_data=None,
                video_url=None,
                retrieval_key=None,
                format=None,
            )

        content_vo = ContentToModerateVo(
            content_id=model.source_model_id,
            author_id=model.user_id,
            policy_routing_key=model.policy_routing_key,
            content_type=content_type,
            content_src=MediaSourceEnum(model.source_app),  # or derive from source_app
            region=model.region or None,
            text_content=text_vo,
            image_content=image_vo,
            video_content=video_vo,
        )

        # 2. ContentSnapshotVo from snapshot (unchanged)
        snapshot_vo = None
        if model.content_snapshot:
            blob = model.content_snapshot.content_blob
            if blob:
                # ... existing snapshot logic remains the same ...
                pass

        # 3. ContentFingerprintVo - query FingerprintModel by case_id
        fingerprint_vo = None
        try:
            fp = FingerprintModel.objects.get(case_id=model.case_id)
            fingerprint_vo = ContentFingerprintVo(
                fingerprint_hash=fp.fingerprint_hash,
                case_id=model.case_id,
                content_type=fp.content_type,
                policy_routing_key=fp.policy_routing_key,
                provider_used=ModerationProviderEnum(fp.provider_used),
                decision_outcome=DecisionEnum(fp.decision_outcome),
                confidence_score=fp.confidence_score,
                created_at=fp.created_at,
                expires_at=fp.expires_at,
                value=fp.fingerprint_hash,
            )
        except FingerprintModel.DoesNotExist:
            pass

        # 4. Decision, Confidence, Action, Provider (unchanged)
        decision_vo = None
        if model.decision:
            decision_vo = ModerationDecisionVo(
                outcome=DecisionEnum(model.decision.outcome),
                reason_code=model.decision.reason_code,
                note=model.decision.note,
            )

        confidence_vo = ConfidenceScoreVo(value=model.confidence_score) if model.confidence_score is not None else None

        action_vo = None
        if model.action:
            action_vo = ModerationActionVo(
                action_type=ModerationActionEnum(model.action.action_type),
                visibility_effect=VisibilityEffectEnum(model.action.visibility_effect),
                reason=model.action.reason,
            )

        provider_used = ModerationProviderEnum(model.provider_used) if model.provider_used else None

        # 5. Build aggregate root
        case = ModerationCase(
            case_id=model.case_id,
            user_id=model.user_id,
            content=content_vo,
            policy_routing_key=model.policy_routing_key,
            content_type=model.content_type,
            region=model.region,
            status=CaseStatusEnum(model.status),
            action=action_vo,
            decision=decision_vo,
            confidence_score=confidence_vo,
            provider_used=provider_used,
            created_at=model.created_at,
            decided_at=model.decided_at,
            content_snapshot=snapshot_vo,
            content_fingerprint=fingerprint_vo,
            appeal=None,
            attempts=[],
        )

        # 6. Appeal (unchanged)
        if model.appeal:
            appeal_model = model.appeal
            case.appeal = AppealEntity(
                appeal_id=appeal_model.appeal_id,
                submitted_by=appeal_model.submitted_by,
                reason=appeal_model.reason,
                submitted_at=appeal_model.submitted_at,
                status=AppealStatusEnum(appeal_model.status),
            )

        # 7. Attempts (unchanged)
        for attempt_model in model.attempts.all():
            case.attempts.append(ModerationAttemptEntity(
                attempt_id=attempt_model.attempt_id,
                moderator_id=attempt_model.moderator_id,
                decision=attempt_model.decision,
                note=attempt_model.note,
                attempted_at=attempt_model.attempted_at,
                resolved_at=attempt_model.resolved_at,
                resolution_note=attempt_model.resolution_note,
            ))

        return case