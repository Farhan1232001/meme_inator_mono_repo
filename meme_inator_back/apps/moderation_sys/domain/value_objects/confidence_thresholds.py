# domain/value_objects/confidence_thresholds.py
from dataclasses import dataclass

from apps.moderation_sys.domain.enums.moderation_enums import ConfidenceBandEnum
from apps.moderation_sys.domain.value_objects.confidence_score import ConfidenceScoreVo


@dataclass(frozen=True)
class ConfidenceThresholdsVo:
    """
    Risk-based confidence thresholds for automated moderation decisions.
    
    Models how most production moderation APIs work:
    Higher scores indicate greater violation risk.
    
    Risk Spectrum:
    
        0%                                                            100%
        ├────────────────┬──────────────────────┬───────────────────────┤
        │  Auto Accept   │   Human Review       │    Auto Reject         │
        │  (Low Risk)    │   (Grey Zone)        │    (High Risk)         │
        └────────────────┴──────────────────────┴───────────────────────┘
                         ^                      ^
                         │                      │
                  low_risk_threshold    high_risk_threshold
    
    Decision Logic:
        score < low_risk_threshold  → ACCEPT (clearly safe)
        score >= high_risk_threshold → REJECT (clearly violating)
        Otherwise                    → FLAG for human review
    
    Examples with standard thresholds (0.3, 0.7):
        - Score 0.1 → Low risk → Auto-accept
        - Score 0.5 → Grey zone → Human review  
        - Score 0.9 → High risk → Auto-reject
    
    Invariants:
        - 0 <= low_risk_threshold <= high_risk_threshold <= 1.0
        - low_risk_threshold < high_risk_threshold (must have grey zone)
    """
    
    high_risk_threshold: float    # Scores >= this → reject
    low_risk_threshold: float     # Scores < this → accept
    grey_zone_min: float          # Equal to low_risk_threshold (for backward compat)
    
    def __post_init__(self):
        if not (0 <= self.low_risk_threshold < self.high_risk_threshold <= 1.0):
            raise ValueError(
                f"Thresholds must satisfy: 0 <= {self.low_risk_threshold} < "
                f"{self.high_risk_threshold} <= 1.0"
            )
        
        if self.grey_zone_min != self.low_risk_threshold:
            raise ValueError(
                f"grey_zone_min ({self.grey_zone_min}) must equal "
                f"low_risk_threshold ({self.low_risk_threshold})"
            )
    
    def classify_confidence(self, score: ConfidenceScoreVo) -> ConfidenceBandEnum:
        """
        Classify a risk score into a confidence band.
        
        Args:
            score: Risk score from moderation API (higher = more violating)
            
        Returns:
            HIGH band if score >= high_risk_threshold (clear violation)
            LOW band if score < low_risk_threshold (clearly safe)
            GREY band otherwise (uncertain, needs human review)
        """
        if score.value >= self.high_risk_threshold:
            return ConfidenceBandEnum.HIGH  # High risk → reject
        elif score.value < self.low_risk_threshold:
            return ConfidenceBandEnum.LOW   # Low risk → accept
        else:
            return ConfidenceBandEnum.GREY  # Grey zone → human review
    
    @property
    def high_confidence_min(self) -> float:
        """Backward compatibility alias for high_risk_threshold."""
        return self.high_risk_threshold
    
    @property
    def low_confidence_max(self) -> float:
        """Backward compatibility alias for low_risk_threshold."""
        return self.low_risk_threshold