# domain/value_objects/confidence_score.py
from dataclasses import dataclass

@dataclass(frozen=True)
class ConfidenceScoreVo:
    value: float

    def is_high_confidence(self, threshold: float) -> bool:
        return self.value >= threshold

    def is_low_confidence(self, threshold: float) -> bool:
        return self.value <= threshold