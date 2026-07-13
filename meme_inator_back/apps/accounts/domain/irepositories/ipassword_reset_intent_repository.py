# apps/accounts/domain/repositories/ipassword_reset_intent_repository.py
from typing import Optional
from uuid import UUID
from core.results import Result
from apps.accounts.domain.entities.password_reset_intent_entity import PasswordResetIntentEntity

class IPasswordResetIntentRepository:
    def create(self, intent: PasswordResetIntentEntity) -> Result[PasswordResetIntentEntity]: ...
    def get_by_challenge(self, challenge_code: str) -> Optional[PasswordResetIntentEntity]: ...
    def mark_consumed(self, intent_id: UUID) -> Result[None]: ...
