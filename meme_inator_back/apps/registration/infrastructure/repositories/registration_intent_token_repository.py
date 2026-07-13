# apps/registration/repositories/registration_repository.py
from apps.registration.infrastructure.models.registration_intent_token_model import RegistrationIntentTokenModel
from apps.registration.mappers import RegistrationIntentTokenMapper
from apps.registration.domain.entities.registration_intent_token_entity import RegistrationIntentTokenEntity
from core.results import Result, Ok, NotOk, Error
from typing import Optional
from uuid import UUID
from django.db import IntegrityError
from datetime import datetime, timezone

class RegistrationIntentTokenRepository:

    def save_token(self, entity: RegistrationIntentTokenEntity) -> Result[RegistrationIntentTokenEntity]:
        try:
            model = RegistrationIntentTokenMapper.to_model(entity)
            model.save()
            return Ok(RegistrationIntentTokenMapper.to_entity(model))
        except IntegrityError as e:
            # token has unique constraint on it and IntegrityErrpr is thrown if constraint is violated. 
            return NotOk(message="Token already exists", static_msg="TOKEN_EXISTS", status_code=400)
        except Exception as e:
            return Error(message="Failed to save token", exception=e)

    def get_by_token(self, token: str) -> Result[Optional[RegistrationIntentTokenEntity]]:
        try:
            model = RegistrationIntentTokenModel.objects.filter(token=token).first()
            if not model:
                return NotOk(message="Token not found", static_msg="TOKEN_NOT_FOUND", status_code=404)
            return Ok(RegistrationIntentTokenMapper.to_entity(model))
        except Exception as e:
            return Error(message="Failed to fetch token", exception=e)

    def mark_consumed(self, token: str) -> Result[RegistrationIntentTokenEntity]:
        try:
            result = self.get_by_token(token)
            if isinstance(result, NotOk) or isinstance(result, Error):
                return result

            entity = result.value
            entity = RegistrationIntentTokenEntity(
                id=entity.id,
                user_id=entity.user_id,
                token=entity.token,
                expires_at=entity.expires_at,
                consumed=True,
                created_at=entity.created_at,
                consumed_at=datetime.now(timezone.utc)
            )
            model = RegistrationIntentTokenModel.objects.get(token=token)
            model.consumed = True
            model.consumed_at = entity.consumed_at
            model.save()
            return Ok(entity)
        except Exception as e:
            return Error(message="Failed to mark token consumed", exception=e)

    def delete_token(self, token: str) -> Result[bool]:
        try:
            deleted, _ = RegistrationIntentTokenModel.objects.filter(token=token).delete()
            if deleted == 0:
                return NotOk(message="Token not found", static_msg="TOKEN_NOT_FOUND", status_code=404)
            return Ok(True)
        except Exception as e:
            return Error(message="Failed to delete token", exception=e)
