# domain/aggregates/moderation_case.py

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID, uuid7

from apps.moderation_sys.domain.enums.moderation_enums import (
    CaseStatusEnum,
    ModerationProviderEnum,
    DecisionEnum,
    AppealStatusEnum,
    AppealOutcomeEnum,
    ModerationActionEnum,
    VisibilityEffectEnum,
)
from apps.moderation_sys.domain.value_objects.content_to_mod.content_to_moderate import ContentToModerateVo
from apps.moderation_sys.domain.value_objects.content_snapshot_vo import ContentSnapshotVo
from apps.moderation_sys.domain.value_objects.content_fingerprint import ContentFingerprintVo
from apps.moderation_sys.domain.value_objects.moderation_decision import ModerationDecisionVo
from apps.moderation_sys.domain.value_objects.confidence_score import ConfidenceScoreVo
from apps.moderation_sys.domain.value_objects.moderation_action import ModerationActionVo
from apps.moderation_sys.domain.value_objects.appeal_eligibility_rules import AppealEligibilityRulesVo
from apps.moderation_sys.domain.entities.appeal_entity import AppealEntity
from apps.moderation_sys.domain.entities.moderation_attempt_entity import ModerationAttemptEntity
from apps.moderation_sys.domain.aggregates.policy_definition import PolicyDefinition


@dataclass
class ModerationCase:
    """
    Aggregate Root for moderation cases.
    
    Invariants:
    1. Cannot moderate a case that is already resolved
    2. Cannot appeal a case that is not REJECTED
    3. Cannot appeal more than once
    4. Appeal must be submitted within policy time window
    5. Visibility effect cannot change after moderation
    """
    # Identity
    case_id: UUID

    # Immutable snapshot & fingerprint taken at submission time, as MUST for all cases.
    # Snapshot proof of content state at submission. Fingerprint proof of identity of content. 
    content_snapshot: ContentSnapshotVo
    content_fingerprint: ContentFingerprintVo

    # Who, Whats, & where pertaining the case
    user_id: UUID # User who submitted content for moderation.
    content: ContentToModerateVo
    policy_routing_key: str = ""  # TODO: Should this be here or in ContentToModerate?
    content_type: str = ""      # TODO: Should this be here or in ContentToModerate?
    region: Optional[str] = None    # TODO: Should this be here or in ContentToModerate?

    # Status and Decisions
    status: CaseStatusEnum = CaseStatusEnum.PENDING
    action: Optional[ModerationActionVo] = None
    decision: Optional[ModerationDecisionVo] = None
    confidence_score: Optional[ConfidenceScoreVo] = None
    provider_used: Optional[ModerationProviderEnum] = None

    # Timestamps
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    decided_at: Optional[datetime] = None

    # Embedded Entites
    appeal: Optional[AppealEntity] = None
    attempts: List[ModerationAttemptEntity] = field(default_factory=None)
    


    @classmethod
    def create_moderation_case(
        cls,
        content: ContentToModerateVo,
        user_id: UUID,
        fingerprint: ContentFingerprintVo,
        snapshot: ContentSnapshotVo,
        region: Optional[str] = None,
    ) -> ModerationCase:
        """
        Factory method to create a new moderation case.
        
        Args:
            content: The content to be moderated
            user_id: The author's user ID
            fingerprint: The content fingerprint for deduplication
            snapshot: The immutable content snapshot
            region: Optional region for the content
        """
        return ModerationCase(
            case_id=uuid7(),
            user_id=user_id,
            # Who, Whats, & where pertaining the case
            content=content,
            policy_routing_key=content.policy_routing_key,
            content_type=content.content_type.value,
            region=region,

            # Status and Decisions
            status=CaseStatusEnum.PENDING,
            action=None,
            decision=None,
            confidence_score=None,
            provider_used=None,

            # Timestamps
            created_at=datetime.now(timezone.utc),
            decided_at=None,
            
            # Embedded Entites
            appeal=None,
            attempts=None,
            
            # Immutable snapshot & fingerprint taken at submission time. Every case must have both
            content_snapshot=snapshot,
            content_fingerprint=fingerprint
        )

    def auto_moderate(
        self, 
        decision: ModerationDecisionVo, 
        confidence: ConfidenceScoreVo
    ) -> None:
        """
        Apply automated moderation decision.
        
        Raises:
            ValueError: If case is already resolved
        """
        if self.status != CaseStatusEnum.PENDING:
            raise ValueError("Cannot moderate a case that is already resolved")
        
        self.decision = decision
        self.confidence_score = confidence
        self.decided_at = datetime.now(timezone.utc)
        
        if decision.outcome != DecisionEnum.FLAG:
            self.status = CaseStatusEnum.RESOLVED
        else:
            self.status = CaseStatusEnum.FLAGGED

    def human_moderate(
        self, 
        decision: ModerationDecisionVo, 
        moderator_id: UUID, 
        note: Optional[str] = None
    ) -> None:
        """
        Apply human moderation decision.
        
        Raises:
            ValueError: If case is not in modifiable state
        """
        if self.status not in [CaseStatusEnum.PENDING, CaseStatusEnum.FLAGGED]:
            raise ValueError("Case not in modifiable state")
        
        self.decision = decision
        self.decided_at = datetime.now(timezone.utc)
        
        if decision.outcome != DecisionEnum.FLAG:
            self.status = CaseStatusEnum.RESOLVED
        else:
            self.status = CaseStatusEnum.FLAGGED
        
        self.attempts.append(ModerationAttemptEntity(
            moderator_id=str(moderator_id),
            decision=decision.outcome.value,
            note=note,
            resolved_at=datetime.now(timezone.utc)
        ))

    def submit_appeal(
        self, 
        user_id: UUID, 
        reason: str, 
        eligibility_rules: AppealEligibilityRulesVo
    ) -> None:
        """
        Submit an appeal for a rejected case.
        
        Raises:
            ValueError: If case is not RESOLVED
            ValueError: If decision is not REJECT
            ValueError: If appeal already exists
        """
        if self.status != CaseStatusEnum.RESOLVED:
            raise ValueError("Cannot appeal a case that is not RESOLVED")
        
        if self.decision is None or self.decision.outcome != DecisionEnum.REJECT:
            raise ValueError("Cannot appeal a case that is not REJECTED")
        
        if self.appeal is not None:
            raise ValueError("Cannot appeal more than once")
        
        self.appeal = AppealEntity.submit(self.case_id, user_id, reason, eligibility_rules)
        self.status = CaseStatusEnum.APPEALING

    def resolve_appeal(
        self, 
        outcome: AppealOutcomeEnum, 
        resolved_by: UUID, 
        resolution_note: Optional[str] = None
    ) -> None:
        """
        Resolve a pending appeal.
        
        Raises:
            ValueError: If no pending appeal exists
        """
        if not self.appeal or self.appeal.status != AppealStatusEnum.PENDING:
            raise ValueError("No pending appeal to resolve")
        
        self.appeal.resolve(outcome, resolved_by, resolution_note)
        self.status = CaseStatusEnum.RESOLVED
        
        if outcome == AppealOutcomeEnum.APPROVED:
            self.decision = ModerationDecisionVo(
                outcome=DecisionEnum.ACCEPT,
                reason_code="APPEAL_UPHELD",
                note=f"Appeal approved: {resolution_note or 'No resolution note provided'}"
            )

    def update_visibility_effect(
        self, 
        new_effect: VisibilityEffectEnum
    ) -> None:
        """
        Update the visibility effect of the moderation action.
        Can only be done before moderation is complete.
        
        Raises:
            ValueError: If case is not in PENDING status
        """
        if self.status != CaseStatusEnum.PENDING:
            raise ValueError("Visibility effect cannot change after moderation")
        
        if self.action:
            # Create new action with updated visibility (VO is immutable)
            self.action = ModerationActionVo(
                action_type=self.action.action_type,
                visibility_effect=new_effect,
                reason=self.action.reason
            )
        else:
            self.action = ModerationActionVo(
                action_type=ModerationActionEnum.FLAG_FOR_HUMAN,
                visibility_effect=new_effect,
                reason="Updated visibility effect"
            )
    
    # Query helpers
    def is_pending(self) -> bool:
        return self.status == CaseStatusEnum.PENDING
    
    def is_flagged(self) -> bool:
        return self.status == CaseStatusEnum.FLAGGED
    
    def is_resolved(self) -> bool:
        return self.status == CaseStatusEnum.RESOLVED
    
    def is_appealing(self) -> bool:
        return self.status == CaseStatusEnum.APPEALING
    
    def has_appeal(self) -> bool:
        return self.appeal is not None
