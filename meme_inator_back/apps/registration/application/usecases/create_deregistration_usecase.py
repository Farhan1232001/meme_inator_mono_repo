# apps/registration/application/usecases/create_deregistration_intent_usecase.py
import uuid
import secrets
from datetime import datetime, timedelta, timezone
from core.results import Ok, Result, Error
from django.contrib.auth.hashers import make_password
from meme_inator_back import settings

from apps.registration.domain.entities.deregistration_intent_challenge_entity import DeregistrationIntentChallengeEntity
from apps.registration.domain.iusecases.icreate_deregistration_intent_usecase import ICreateDeregistrationIntentUsecase

class CreateDeregistrationIntentUsecase(ICreateDeregistrationIntentUsecase):

    def execute(self, user_id: uuid.UUID) -> Result[tuple[DeregistrationIntentChallengeEntity, str]]:
        try:
            # generate a short numeric challenge, e.g., 6 digits
            plain_code = str(secrets.randbelow(10**6)).zfill(6)  # e.g., "004321"

            now = datetime.now(timezone.utc)
            # TODO: Check to see if make_password here is ideal? Maybe use some other hash function with your own salt. 
            code_hash = make_password(plain_code)  # use Django hashers

            entity = DeregistrationIntentChallengeEntity(
                id = uuid.uuid7(),
                user_id = user_id,
                code_hash = code_hash,
                expires_at = now + timedelta(seconds=settings.DEREGISTRATION_CHALLENGE_TTL_SECONDS),
                consumed = False,
                created_at = now,
                consumed_at = None
            )

            return Ok((entity, plain_code))
        except Exception as e:
            return Error(message="failed to create deregistration challenge", exception=e)
