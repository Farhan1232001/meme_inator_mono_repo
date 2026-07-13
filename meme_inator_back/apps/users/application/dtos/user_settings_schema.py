from typing import Optional
from pydantic import BaseModel

class UserSettingsSchema(BaseModel):
    email_notifications: bool = True
    push_notifications: bool = True
    default_feed_type: str = "for_you"
