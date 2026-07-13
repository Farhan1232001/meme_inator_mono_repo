# domain/entities/appeal_entity.py
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4, uuid7
from typing import Optional
from ..enums.moderation_enums import AppealStatusEnum, AppealOutcomeEnum
from ..value_objects.appeal_eligibility_rules import AppealEligibilityRulesVo

@dataclass
class AppealEntity:
    appeal_id: UUID = field(default_factory=uuid7)
    submitted_by: UUID = field(default=None)
    reason: str = ""
    submitted_at: datetime = field(default_factory= datetime.now(timezone.utc))
    status: AppealStatusEnum = AppealStatusEnum.PENDING

    @classmethod
    def submit(cls, case_id: UUID, user_id: UUID, reason: str, 
               eligibility_rules: AppealEligibilityRulesVo) -> 'AppealEntity':
        # Eligibility check should be performed before creation
        return cls(
            submitted_by=user_id,
            reason=reason,
            status=AppealStatusEnum.PENDING
        )

    def resolve(self, outcome: AppealOutcomeEnum, resolved_by: UUID, resolution_note: Optional[str] = None):
        if self.status != AppealStatusEnum.PENDING:
            raise ValueError("Appeal already resolved")
        self.status = AppealStatusEnum.APPROVED if outcome == AppealOutcomeEnum.APPROVED else AppealStatusEnum.DENIED

    def expire(self):
        if self.status == AppealStatusEnum.PENDING:
            self.status = AppealStatusEnum.EXPIRED