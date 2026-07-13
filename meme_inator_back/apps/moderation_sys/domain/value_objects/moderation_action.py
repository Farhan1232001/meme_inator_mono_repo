# domain/value_objects/moderation_action.py
from dataclasses import dataclass

from apps.moderation_sys.domain.enums.moderation_enums import ModerationActionEnum, VisibilityEffectEnum

@dataclass(frozen=True)
class ModerationActionVo:
    action_type: ModerationActionEnum
    visibility_effect: VisibilityEffectEnum
    reason: str