from dataclasses import dataclass
from typing import List, Optional

from apps.feeds.domain.entities.duration_window_vo import DurationWindow


@dataclass
class SectionalFeedPageResponseVo:
    """
    Response VO returned to controller:
      - duration_windows: list[DurationWindow]
      - next_cursor: an opaque time-based cursor to fetch the next set of windows
      - has_more: bool flag showing whether more windows exist
    """
    duration_windows: List[DurationWindow]
    next_cursor: Optional[str]
    has_more: bool = False