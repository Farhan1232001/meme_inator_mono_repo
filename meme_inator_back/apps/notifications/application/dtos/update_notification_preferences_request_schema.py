
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from apps.notifications.application.dtos.custom_digest_preferences_schema import CustomDigestPreferencesSchema


class UpdateNotificationPreferencesRequest(BaseModel):
    """Request schema for PATCH /preferences"""
    is_notification_enabled: Optional[bool] = None
    is_push_enabled: Optional[bool] = None
    is_email_enabled: Optional[bool] = None
    is_in_app_enabled: Optional[bool] = None
    is_new_messages_enabled: Optional[bool] = None
    is_replies_to_user_enabled: Optional[bool] = None
    is_comment_to_user_enabled: Optional[bool] = None
    is_sub_to_user_notification_enabled: Optional[bool] = None
    muted_notification_types: Optional[List[str]] = None
    snooze_until: Optional[datetime] = None
    custom_digest_preferences: Optional[CustomDigestPreferencesSchema] = None
