from dataclasses import dataclass


@dataclass(frozen=True)
class ReputationImpactVo:
    accept_points_delta: int
    reject_points_delta: int
    appeal_upheld_points_return: int
    appeal_denied_penalty: int

    def points_for_accept(self) -> int:
        return self.accept_points_delta

    def points_for_reject(self) -> int:
        return self.reject_points_delta

    def points_for_appeal_upheld(self) -> int:
        return self.appeal_upheld_points_return

    def points_for_appeal_denied(self) -> int:
        return self.appeal_denied_penalty