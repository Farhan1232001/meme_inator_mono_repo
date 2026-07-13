# apps/registration/mappers/registration_intent_token_mapper.py
from apps.registration.domain.entities.registration_intent_token_entity import RegistrationIntentTokenEntity
from apps.registration.infrastructure.models.registration_intent_token_model import RegistrationIntentTokenModel

class RegistrationIntentTokenMapper:
    
    @staticmethod
    def to_entity(model: RegistrationIntentTokenModel) -> RegistrationIntentTokenEntity:
        return RegistrationIntentTokenEntity(
            id=model.id,
            user_id=model.user_id,
            token=model.token,
            expires_at=model.expires_at,
            consumed=model.consumed,
            created_at=model.created_at,
            consumed_at=model.consumed_at,
        )
    
    @staticmethod
    def to_model(entity: RegistrationIntentTokenEntity) -> RegistrationIntentTokenModel:
        model = RegistrationIntentTokenModel(
            id=entity.id,
            user_id=entity.user_id,
            token=entity.token,
            expires_at=entity.expires_at,
            consumed=entity.consumed,
            created_at=entity.created_at,
            consumed_at=entity.consumed_at,
        )
        return model


# apps/registration/mappers/deregistration_intent_challenge_mapper.py
from apps.registration.domain.entities.deregistration_intent_challenge_entity import DeregistrationIntentChallengeEntity
from apps.registration.infrastructure.models.deregistration_intent_challenge_model import DeregistrationIntentChallengeModel

class DeregistrationIntentChallengeMapper:

    @staticmethod
    def to_entity(model: DeregistrationIntentChallengeModel) -> DeregistrationIntentChallengeEntity:
        return DeregistrationIntentChallengeEntity(
            id=model.id,
            user_id=model.user_id,
            code_hash=model.code_hash,
            expires_at=model.expires_at,
            consumed=model.consumed,
            created_at=model.created_at,
            consumed_at=model.consumed_at,
        )

    @staticmethod
    def to_model(entity: DeregistrationIntentChallengeEntity) -> DeregistrationIntentChallengeModel:
        return DeregistrationIntentChallengeModel(
            id=entity.id,
            user_id=entity.user_id,
            code_hash=entity.code_hash,
            expires_at=entity.expires_at,
            consumed=entity.consumed,
            created_at=entity.created_at,
            consumed_at=entity.consumed_at,
        )
