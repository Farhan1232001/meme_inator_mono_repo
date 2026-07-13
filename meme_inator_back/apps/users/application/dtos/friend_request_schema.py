from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from apps.users.domain.entities.user_entity import UserEntity

class FriendRequestSchema(BaseModel):
    id: str
    sender: UserEntity
    receiver: UserEntity
    status: str
    created_at: datetime
