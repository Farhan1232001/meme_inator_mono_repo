# apps/accounts/domain/entities/password_reset_intent_entity.py
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class PasswordResetIntentEntity:
    id: UUID
    user_id: UUID
    challenge_hash: str
    expires_at: datetime
    consumed: bool = False
