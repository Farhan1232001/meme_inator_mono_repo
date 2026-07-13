# apps/moderation_sys/domain/value_objects/moderation_response.py

from dataclasses import dataclass
from typing import Mapping, Optional
from apps.moderation_sys.domain.enums.moderation_enums import ModerationProviderEnum


@dataclass(frozen=True)
class ModerationResponseVo:
    """
    Unified moderation provider response.

    Represents provider output before internal
    moderation policy/routing decisions.
    """
    # REQUIRED fields (no defaults) - MUST come first
    provider: ModerationProviderEnum
    flagged: bool
    categories: Mapping[str, bool]
    category_scores: Mapping[str, float]
    model: str | None  # Can be None, but still required to be specified
    
    # OPTIONAL fields (with defaults) - MUST come after all required fields
    raw_response_id: Optional[str] = None
    applied_input_types: Optional[Mapping[str, list[str]]] = None

    @property
    def highest_category(self) -> str | None:
        if not self.category_scores:
            return None

        return max(
            self.category_scores,
            key=self.category_scores.get,
        )

    @property
    def highest_score(self) -> float:
        if not self.category_scores:
            return 0.0

        return max(self.category_scores.values())