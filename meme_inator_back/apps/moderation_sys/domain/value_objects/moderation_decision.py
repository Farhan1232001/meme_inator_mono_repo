# domain/value_objects/moderation_decision.py
from dataclasses import dataclass
from typing import Optional
from ..enums.moderation_enums import DecisionEnum

@dataclass(frozen=True)
class ModerationDecisionVo:
    outcome: DecisionEnum
    reason_code: Optional[str] = None
    note: Optional[str] = None