from typing import Optional, List
from ninja import Schema


class GfPageRequestSchema(Schema):
    """

    """
    type: str
    cursor: Optional[str] = None
    page_size: int = 10
