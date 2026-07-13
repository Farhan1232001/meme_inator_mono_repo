import uuid
import secrets
from datetime import datetime, timedelta, timezone
from apps.registration.domain.entities.registration_intent_token_entity import RegistrationIntentTokenEntity
from apps.registration.domain.iusecases.icreate_registration_intent_token_usecase import ICreateRegistrationIntentTokenUsecase
from core.results import Ok, Result
from meme_inator_back import settings

class CreateRegistrationIntentTokenUsecase(ICreateRegistrationIntentTokenUsecase):
    def execute(self, user_id: uuid.UUID) -> Result[RegistrationIntentTokenEntity]:
        
        now = datetime.now(timezone.utc)
        return Ok(RegistrationIntentTokenEntity(
            id          = uuid.uuid7,
            user_id     = user_id,
            token       = secrets.token_urlsafe(32),
            expires_at  = now + timedelta(seconds=settings.REGISTRATION_TOKEN_TTL_SECONDS),
            consumed    = False,
            created_at  = now,
            consumed_at = None
        ))
