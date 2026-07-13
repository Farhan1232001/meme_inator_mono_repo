from typing import Optional

from pydantic import BaseModel


class SuccessResponseSchema(BaseModel):
    success: bool = True
    message: Optional[str] = None
    marked_count: Optional[int] = None

    class Config:
        json_schema_extra = {"example": {"success": True, "marked_count": 5}}

