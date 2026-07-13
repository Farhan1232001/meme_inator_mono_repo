from typing import List, Optional

from ninja import Schema

from apps.feeds.application.dtos.duration_window_schema import DurationWindowSchema


class SfPageResponseSchema(Schema):
    next_cursor: Optional[str] = None
    has_more: bool = False
    duration_windows: List[DurationWindowSchema]
    