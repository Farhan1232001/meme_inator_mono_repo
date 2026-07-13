# domain/value_objects/appeal_eligibility_rules.py
from dataclasses import dataclass
from typing import List
from datetime import datetime, timedelta, timezone
from ..enums.moderation_enums import DecisionEnum

@dataclass(frozen=True)
class AppealEligibilityRulesVo:
    time_limit_hours: int
    requires_reason: bool
    appealable_decisions: List[DecisionEnum]
    max_appeals_per_user_per_day: int

    def is_eligible(self, case, user_history: dict) -> bool:
        # Implement eligibility checks
        if case.decision.outcome not in self.appealable_decisions:
            return False
        if datetime.now(timezone.utc) > case.decided_at + timedelta(hours=self.time_limit_hours):
            return False
        # Check user appeal count for the day
        return True