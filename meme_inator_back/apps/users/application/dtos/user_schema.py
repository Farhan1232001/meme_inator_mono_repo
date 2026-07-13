from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

class UserSchema(BaseModel):
    id: UUID
    username: str
    email: str
    is_online: bool
    is_verified: bool
    is_banned: bool
    date_joined: datetime


    # User related Entitlements
    is_pro_user: bool
