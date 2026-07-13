from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class WebhookRetryPolicyVo:
    max_retries: int = 3
    initial_delay_seconds: int = 2
    backoff_multiplier: float = 2.0 # e.g. 2.0
    max_delay_seconds: int = 5

    def next_delay(self, attempt_number: int) -> timedelta:
        delay = self.initial_delay_seconds * (self.backoff_multiplier ** (attempt_number - 1))
        delay = min(delay, self.max_delay_seconds)
        return timedelta(seconds=delay)

    def can_retry(self, attempt_number: int) -> bool:
        return attempt_number < self.max_retries