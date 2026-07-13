from typing import Optional
from ninja import Schema


class SfPageRequestSchema(Schema):
    feed_type: str
    duration_unit: str
    duration_window_size: int = 3
    cursor: Optional[str] = None
    requesting_user_id: Optional[str] = None