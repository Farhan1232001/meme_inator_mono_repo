from dataclasses import dataclass


@dataclass(frozen=True)
class ErrorRateVo:
    total_requests: int
    total_failures: int

    def rate(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return self.total_failures / self.total_requests

    def with_success(self) -> "ErrorRateVo":
        return ErrorRateVo(
            total_requests=self.total_requests + 1,
            total_failures=self.total_failures,
        )

    def with_failure(self) -> "ErrorRateVo":
        return ErrorRateVo(
            total_requests=self.total_requests + 1,
            total_failures=self.total_failures + 1,
        )