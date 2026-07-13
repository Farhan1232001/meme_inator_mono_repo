from typing import Any, Dict, Optional

from pydantic import BaseModel


class NotificationPayloadSchema(BaseModel):
    title: str
    body: Optional[str] = None
    extra: Optional[Dict[str, Any]] = None
    url: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "John liked your post",
                "body": "John liked 'My awesome post'",
                "extra": {"post_id": "123e4567-e89b-12d3-a456-426614174000"},
                "url": "/posts/123e4567-e89b-12d3-a456-426614174000"
            }
        }
