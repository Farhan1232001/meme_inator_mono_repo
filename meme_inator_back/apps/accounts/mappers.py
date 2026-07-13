# apps/accounts/infrastructure/mappers/password_reset_intent_mapper.py
from apps.accounts.domain.entities.password_reset_intent_entity import (
    PasswordResetIntentEntity,
)
from apps.accounts.infrastructure.models.password_reset_intent_model import (
    PasswordResetIntentModel,
)


class PasswordResetIntentMapper:
    @staticmethod
    def to_model(entity: PasswordResetIntentEntity) -> PasswordResetIntentModel:
        return PasswordResetIntentModel(
            id=entity.id,
            user_id=entity.user_id,
            challenge_hash=entity.challenge_hash,
            expires_at=entity.expires_at,
            consumed=entity.consumed,
        )

    @staticmethod
    def to_entity(model: PasswordResetIntentModel) -> PasswordResetIntentEntity:
        return PasswordResetIntentEntity(
            id=model.id,
            user_id=model.user_id,
            challenge_hash=model.challenge_hash,
            expires_at=model.expires_at,
            consumed=model.consumed,
        )
