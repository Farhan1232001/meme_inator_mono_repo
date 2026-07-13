from datetime import datetime, timezone
from uuid import UUID, uuid4

from apps.moderation_sys.domain.value_objects.error_rate import ErrorRateVo
from apps.moderation_sys.domain.value_objects.sliding_window_metrics import SlidingWindowMetricsVo


class CircuitBreakerStateEnum:
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class ProviderHealth:
    FAILURE_THRESHOLD = 0.5   # TODO: In real sys, should come from PolicyDefinition or seperate ProviderHealthPolicyVo configurable later
    MIN_REQUESTS = 10

    def __init__(
        self,
        provider_name: str,
        error_rate: ErrorRateVo,
        sliding_window_metrics: SlidingWindowMetricsVo,
        circuit_breaker_state: str = CircuitBreakerStateEnum.CLOSED,
        last_state_change: datetime | None = None,
    ):
        self.provider_name = provider_name
        self.error_rate = error_rate
        self.sliding_window_metrics = sliding_window_metrics
        self.circuit_breaker_state = circuit_breaker_state
        self.last_state_change = last_state_change or datetime.now(timezone.utc)

    # -------------------------
    # Commands
    # -------------------------

    def record_success(self) -> None:
        self.error_rate = self.error_rate.with_success()
        self.sliding_window_metrics.record(True)

        if self.circuit_breaker_state == CircuitBreakerStateEnum.HALF_OPEN:
            self._close_circuit()

    def record_failure(self) -> None:
        self.error_rate = self.error_rate.with_failure()
        self.sliding_window_metrics.record(False)

        if self._should_open_circuit():
            self._open_circuit()

    def attempt_reset(self) -> None:
        if self.circuit_breaker_state == CircuitBreakerStateEnum.OPEN:
            self.circuit_breaker_state = CircuitBreakerStateEnum.HALF_OPEN
            self.last_state_change = datetime.now(timezone.utc)

    # -------------------------
    # Internal Logic
    # -------------------------

    def _should_open_circuit(self) -> bool:
        if len(self.sliding_window_metrics.results) < self.MIN_REQUESTS:
            return False

        return (
            self.sliding_window_metrics.failure_rate()
            >= self.FAILURE_THRESHOLD
        )

    def _open_circuit(self) -> None:
        self.circuit_breaker_state = CircuitBreakerStateEnum.OPEN
        self.last_state_change = datetime.now(timezone.utc)

    def _close_circuit(self) -> None:
        self.circuit_breaker_state = CircuitBreakerStateEnum.CLOSED
        self.last_state_change = datetime.now(timezone.utc)

    # -------------------------
    # Queries
    # -------------------------

    def is_available(self) -> bool:
        return self.circuit_breaker_state != CircuitBreakerStateEnum.OPEN