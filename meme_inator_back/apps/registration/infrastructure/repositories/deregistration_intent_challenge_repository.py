# apps/registration/infrastructure/repositories/deregistration_intent_challenge_repository.py
from typing import Optional
from uuid import UUID
from datetime import datetime, timezone
from django.db import IntegrityError
from core.results import Result, Ok, NotOk, Error

from apps.registration.infrastructure.models.deregistration_intent_challenge_model import DeregistrationIntentChallengeModel
from apps.registration.mappers import DeregistrationIntentChallengeMapper
from apps.registration.domain.entities.deregistration_intent_challenge_entity import DeregistrationIntentChallengeEntity

class DeregistrationIntentChallengeRepository:

    def create(self, entity: DeregistrationIntentChallengeEntity) -> Result[DeregistrationIntentChallengeEntity]:
        try:
            model = DeregistrationIntentChallengeMapper.to_model(entity)
            model.save()
            return Ok(DeregistrationIntentChallengeMapper.to_entity(model))
        except IntegrityError as e:
            return NotOk(message="Challenge already exists", static_msg="CHALLENGE_EXISTS", status_code=400)
        except Exception as e:
            return Error(message="Failed to save challenge", exception=e)

    def get_active_for_user(self, user_id: UUID) -> Result[Optional[DeregistrationIntentChallengeEntity]]:
        try:
            model = DeregistrationIntentChallengeModel.objects.filter(user_id=user_id, consumed=False).order_by("-created_at").first()
            if not model:
                return NotOk(message="No active deregistration intent", static_msg="NO_PENDING_DEREGISTRATION", status_code=404)
            return Ok(DeregistrationIntentChallengeMapper.to_entity(model))
        except Exception as e:
            return Error(message="Failed to fetch challenge", exception=e)

    def mark_consumed(self, challenge_id: UUID) -> Result[DeregistrationIntentChallengeEntity]:
        try:
            model = DeregistrationIntentChallengeModel.objects.get(id=challenge_id)
            model.mark_consumed()
            return Ok(DeregistrationIntentChallengeMapper.to_entity(model))
        except DeregistrationIntentChallengeModel.DoesNotExist:
            return NotOk(message="Challenge not found", static_msg="CHALLENGE_NOT_FOUND", status_code=404)
        except Exception as e:
            return Error(message="Failed to mark challenge consumed", exception=e)

    def delete(self, challenge_id: UUID) -> Result[bool]:
        try:
            deleted, _ = DeregistrationIntentChallengeModel.objects.filter(id=challenge_id).delete()
            if deleted == 0:
                return NotOk(message="Challenge not found", static_msg="CHALLENGE_NOT_FOUND", status_code=404)
            return Ok(True)
        except Exception as e:
            return Error(message="Failed to delete challenge", exception=e)
