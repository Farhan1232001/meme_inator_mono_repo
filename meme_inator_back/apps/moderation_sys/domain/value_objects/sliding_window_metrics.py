from dataclasses import dataclass, field
from collections import deque


# TODO: Value objects are non-mutable. This class is mutable. 
@dataclass
class SlidingWindowMetricsVo:
    window_size: int
    results: deque = field(default_factory=deque)

    def record(self, success: bool) -> None:
        if len(self.results) >= self.window_size:
            self.results.popleft()
        self.results.append(success)

    def failure_rate(self) -> float:
        if not self.results:
            return 0.0
        failures = sum(1 for r in self.results if not r)
        return failures / len(self.results)