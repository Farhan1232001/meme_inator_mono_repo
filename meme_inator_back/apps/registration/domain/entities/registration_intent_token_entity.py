from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import Optional

# TODO: Add failed_attepts feature / counter. 
@dataclass(frozen=True)
class RegistrationIntentTokenEntity:
    id: UUID
    user_id: UUID
    token: str
    expires_at: datetime
    consumed: bool
    created_at: datetime
    consumed_at: Optional[datetime] = None