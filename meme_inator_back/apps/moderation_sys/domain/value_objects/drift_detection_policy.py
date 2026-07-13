from dataclasses import dataclass


@dataclass(frozen=True)
class DriftDetectionPolicyVo:
    confidence_delta_threshold: float  # e.g. 0.2
    decision_change_required: bool
    min_samples: int

    def is_drift(
        self,
        previous_decision: str,
        current_decision: str,
        confidence_delta: float,
        sample_count: int,
    ) -> bool:
        if sample_count < self.min_samples:
            return False

        if self.decision_change_required and previous_decision == current_decision:
            return False

        return abs(confidence_delta) >= self.confidence_delta_threshold