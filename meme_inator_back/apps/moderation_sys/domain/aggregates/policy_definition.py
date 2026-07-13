# domain/aggregates/policy_definition.py
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid7
from typing import Optional

from apps.moderation_sys.domain.enums.moderation_enums import ConfidenceBandEnum
from apps.moderation_sys.domain.value_objects.appeal_eligibility_rules import AppealEligibilityRulesVo
from apps.moderation_sys.domain.value_objects.confidence_score import ConfidenceScoreVo
from apps.moderation_sys.domain.value_objects.confidence_thresholds import ConfidenceThresholdsVo
from apps.moderation_sys.domain.value_objects.drift_detection_policy import DriftDetectionPolicyVo
from apps.moderation_sys.domain.value_objects.reputation_impact import ReputationImpactVo
from apps.moderation_sys.domain.value_objects.webhook_retry_policy import WebhookRetryPolicyVo


@dataclass
class PolicyDefinition:
    """
    Defines how a policy should behave. Each policy definition has a routing_key which uses 
    <feature>:<override>:<content_type> as the schema. 
    ex. comments:pro_user:text
    """
    policy_id: UUID = field(default_factory=uuid7)
    routing_key: str = "global_default"
    version: int = -1
    confidence_thresholds: ConfidenceThresholdsVo = None
    appeal_eligibility_rules: AppealEligibilityRulesVo = None
    reputation_impact: ReputationImpactVo = None
    webhook_retry_policy: WebhookRetryPolicyVo = None
    drift_detection_policy: DriftDetectionPolicyVo = None
    active_from: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    active_to: Optional[datetime] = None
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def update_thresholds(self, new_thresholds: ConfidenceThresholdsVo, updated_by: UUID):
        self.confidence_thresholds = new_thresholds
        self.updated_at = datetime.now(timezone.utc)
        self.version += 1

    def update_appeal_rules(self, new_rules: AppealEligibilityRulesVo, updated_by: UUID):
        self.appeal_eligibility_rules = new_rules
        self.updated_at = datetime.now(timezone.utc)
        self.version += 1

    def activate(self, activated_by: UUID):
        self.active_from = datetime.now(timezone.utc)
        self.active_to = None
        self.updated_at = datetime.now(timezone.utc)

    def deactivate(self, deprecated_by: UUID):
        self.active_to = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def is_active(self) -> bool:
        now = datetime.now(timezone.utc)
        return self.active_from <= now and (self.active_to is None or self.active_to > now)

    def classify_confidence(self, score: ConfidenceScoreVo) -> ConfidenceBandEnum:
        return self.confidence_thresholds.classify_confidence(score)

    def is_appeal_eligible(self, case, user_history: dict) -> bool:
        return self.appeal_eligibility_rules.is_eligible(case, user_history)