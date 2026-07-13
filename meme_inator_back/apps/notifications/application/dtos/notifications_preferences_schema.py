from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from apps.notifications.application.dtos.custom_digest_preferences_schema import CustomDigestPreferencesSchema


class NotificationPreferencesSchema(BaseModel):
    user_id: UUID
    is_notification_enabled: bool = True
    is_push_enabled: bool = True
    is_email_enabled: bool = True
    is_in_app_enabled: bool = True
    is_new_messages_enabled: bool = True
    is_replies_to_user_enabled: bool = True
    is_comment_to_user_enabled: bool = True
    is_sub_to_user_notification_enabled: bool = True
    muted_notification_types: List[str] = []
    snooze_until: Optional[datetime] = None
    custom_digest_preferences: Optional[CustomDigestPreferencesSchema] = None

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "is_notification_enabled": True,
                "is_push_enabled": True,
                "is_email_enabled": False,
                "is_in_app_enabled": True,
                "is_new_messages_enabled": True,
                "is_replies_to_user_enabled": True,
                "is_comment_to_user_enabled": True,
                "is_sub_to_user_notification_enabled": True,
                "muted_notification_types": ["disliked", "system_alerted"],
                "snooze_until": None,
                "custom_digest_preferences": None
            }
        }
