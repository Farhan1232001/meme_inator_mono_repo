# application/usecases/submit_moderation_case.py

from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid7
from typing import Optional
from apps.moderation_sys.application.schemas.moderation_submission_request import ModerationSubmissionRequestSchema
from apps.moderation_sys.domain.aggregates.moderation_case import ModerationCase
from apps.moderation_sys.domain.aggregates.policy_definition import PolicyDefinition
from apps.moderation_sys.domain.enums.media_src_enum import MediaSourceEnum
from apps.moderation_sys.domain.enums.media_type_enums import MediaTypeEnum
from apps.moderation_sys.domain.irepositories.moderation_case_repository import IModerationCaseRepository
from apps.moderation_sys.domain.services.content_fetcher.content_fetcher import ContentNotFoundError, IContentFetcher
from apps.moderation_sys.domain.services.fingerprint_service import FingerprintDomainService
from apps.moderation_sys.domain.services.policy_registry_service import PolicyRegistryService
from apps.moderation_sys.domain.value_objects.content_snapshot_vo import (
    ContentSnapshotVo,
    TextSnapshotVo,
    ImageSnapshotVo,
    VideoSnapshotVo,
)
from apps.moderation_sys.domain.value_objects.content_to_mod.content_to_moderate import ContentToModerateVo
from apps.moderation_sys.domain.value_objects.content_fingerprint import ContentFingerprintVo
from core.results import Error, NotOk, Ok, Result
from apps.moderation_sys.domain.enums.moderation_enums import ModerationProviderEnum, DecisionEnum

class SubmitModerationCaseUsecase:
    """
    Orchestrates the creation of a new moderation case.
    
    Flow:
    1. Build ContentToModerateVo from submission schema
    2. Look up active policy - return NotOk if not found
    3. Fetch content and create snapshot based on content type/source
    4. Generate content fingerprint
    5. Create and persist ModerationCase with rollback support
    """
    
    def __init__(
        self,
        case_repo: IModerationCaseRepository,
        policy_registry: PolicyRegistryService,
        content_fetcher: IContentFetcher,
        fingerprint_service: FingerprintDomainService,
    ):
        self._case_repo = case_repo
        self._policy_registry = policy_registry
        self._content_fetcher = content_fetcher
        self._fingerprint_service = fingerprint_service

    def execute(self, content_to_moderate: ContentToModerateVo) -> Result[ModerationCase]:
        """Execute the use case with the Ninja schema as input."""
        try:
            # Step 1: Build ContentToModerateVo from the submission schema
            # content_vo:ContentToModerateVo = self._build_content_vo(submission)
            content:ContentToModerateVo = content_to_moderate
            
            # Step 2: Look up active policy
            policy:PolicyDefinition = self._policy_registry.lookup_active_policy(content.policy_routing_key)
            if not policy or not policy.is_active():
                return NotOk(
                    message=f"No active policy found for routing key: {content.policy_routing_key}",
                    static_msg="POLICY_NOT_FOUND"
                )
            
            # Step 3: Generate content fingerprint
            fingerprint:ContentFingerprintVo = self._create_fingerprint(content)
            if fingerprint is None:
                return Error(
                    message=f"Fingerprint failed to generate - SUBMISSION FAILED",
                    static_msg="FINGERPRINT_GEN_FAILED"
                )
            
            # Step 4: Create content snapshot
            content_snapshot:ContentSnapshotVo = self._create_content_snapshot(content, fingerprint)
            if content_snapshot.is_empty():
                return NotOk(
                    message="Content snapshot is empty - no content to moderate",
                    static_msg="EMPTY_CONTENT"
                )
            
            # Step 5: Create and persist ModerationCase
            new_case:ModerationCase = ModerationCase.create_moderation_case(
                content=content,
                user_id=content.author_id,
                fingerprint=fingerprint,
                snapshot=content_snapshot,
                region=content.region
            )
            
            # Step 6: Persist (transaction with rollback handled by repository)
            saved_case:Result[ModerationCase] = self._case_repo.save(new_case)
            return saved_case
            
        except ContentNotFoundError as e:
            return NotOk(message=str(e), static_msg="CONTENT_NOT_FOUND")
        except Exception as e:
            return Error(message="Failed to submit moderation case", exception=e)



    def _create_content_snapshot(self, content_vo: ContentToModerateVo, fingerprint:ContentFingerprintVo) -> ContentSnapshotVo:
        """Create an immutable snapshot of the content at submission time."""
        try:
            # Fetch content metadata
            text, image_url, video_url = self._content_fetcher.fetch_content(content_vo)
        except ContentNotFoundError:
            raise  # Let the caller handle this
        
        # Calculate content size
        content_size = self._calculate_content_size(content_vo, text)
        
        # Build type-specific snapshot components
        text_snapshot = None
        image_snapshot = None
        video_snapshot = None
        
        if content_vo.content_type == MediaTypeEnum.TEXT:
            text_snapshot = TextSnapshotVo(
                text=text or "",
                language=None
            )
        elif content_vo.content_type == MediaTypeEnum.IMG:
            image_snapshot = ImageSnapshotVo(
                image_url=image_url,
                retrieval_key=content_vo.image_content.retrieval_key if content_vo.image_content else None,
                format=content_vo.image_content.format if content_vo.image_content else None
            )
        elif content_vo.content_type == MediaTypeEnum.VIDEO:
            video_snapshot = VideoSnapshotVo(
                video_url=video_url,
                retrieval_key=content_vo.video_content.retrieval_key if content_vo.video_content else None,
                format=content_vo.video_content.format if content_vo.video_content else None
            )
        
        return ContentSnapshotVo(
            id=uuid7(),
            fingerprint=fingerprint.value,
            type=content_vo.content_type,
            content_size_bytes=content_size,
            captured_at=datetime.now(timezone.utc),
            text_snapshot=text_snapshot,
            image_snapshot=image_snapshot,
            video_snapshot=video_snapshot
        )

    def _create_fingerprint(self, content_vo: ContentToModerateVo) -> Optional[ContentFingerprintVo]:
        """Create a content fingerprint value object.
        TODO: Instead of creating fingerprint, have a get_or_create_fingerprint method. 
        Also change DjangoModerationCaseRepository.save method to make sure fingerprint only created if its unique. 
        """
        
        fingerprint_hash = self._fingerprint_service.generate(content_vo)
        if fingerprint_hash is None: return None
        now = datetime.now(timezone.utc)
        
        return ContentFingerprintVo(
            fingerprint_hash=fingerprint_hash,
            case_id=UUID(int=0),  # Placeholder, will be updated
            content_type=content_vo.content_type.value,
            policy_routing_key=content_vo.policy_routing_key,
            provider_used=ModerationProviderEnum.OPENAI_API,  # Default
            decision_outcome=DecisionEnum.FLAG,  # Default
            confidence_score=0.0,  # Default
            created_at=now,
            expires_at=now + timedelta(days=30),
            value=fingerprint_hash
        )

    def _calculate_content_size(self, content_vo: ContentToModerateVo, text: Optional[str]) -> Optional[int]:
        """Calculate the size of the content in bytes."""
        if text:
            return len(text.encode('utf-8'))
        elif content_vo.image_content and content_vo.image_content.image_data:
            return len(content_vo.image_content.image_data)
        elif content_vo.video_content and content_vo.video_content.video_data:
            return len(content_vo.video_content.video_data)
        return None

        