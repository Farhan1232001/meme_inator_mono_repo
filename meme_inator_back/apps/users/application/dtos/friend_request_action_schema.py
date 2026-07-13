from pydantic import BaseModel
from typing import Literal

class FriendRequestActionSchema(BaseModel):
    """Schema for accepting or rejecting a friend request."""
    action: Literal["accept", "reject"]