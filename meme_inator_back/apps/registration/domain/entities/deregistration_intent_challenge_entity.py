# apps/registration/domain/entities/deregistration_intent_challenge_entity.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

# TODO: Add failed_attepts feature / counter. 
@dataclass(frozen=True)
class DeregistrationIntentChallengeEntity:
    id: UUID
    user_id: UUID
    code_hash: str
    expires_at: datetime
    consumed: bool
    created_at: datetime
    consumed_at: Optional[datetime] = None
