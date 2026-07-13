# apps/accounts/infrastructure/repositories/password_reset_intent_repository.py
from __future__ import annotations

from typing import Optional
from uuid import UUID
from datetime import datetime, timezone

from django.contrib.auth.hashers import check_password
from django.db import transaction

from apps.accounts.mappers import PasswordResetIntentMapper
from core.results import Ok, NotOk, Error, Result

from apps.accounts.domain.entities.password_reset_intent_entity import (
    PasswordResetIntentEntity,
)
from apps.accounts.domain.irepositories.ipassword_reset_intent_repository import (
    IPasswordResetIntentRepository,
)
from apps.accounts.infrastructure.models.password_reset_intent_model import (
    PasswordResetIntentModel,
)


class PasswordResetIntentRepository(IPasswordResetIntentRepository):
    """
    Django ORM implementation of PasswordResetIntent repository.
    """

    # -------------------------
    # Create
    # -------------------------
    def create(
        self, intent: PasswordResetIntentEntity
    ) -> Result[PasswordResetIntentEntity]:
        try:
            model = PasswordResetIntentModel.objects.create(
                id=intent.id,
                user_id=intent.user_id,
                challenge_hash=intent.challenge_hash,
                expires_at=intent.expires_at,
                consumed=intent.consumed,
            )
            return Ok(
                PasswordResetIntentMapper.to_entity(model)
            )
        except Exception as e:
            return Error(
                message="failed to create password reset intent",
                exception=e,
            )

    # -------------------------
    # Lookup by challenge code
    # -------------------------
    def get_by_challenge(
        self, challenge_code: str
    ) -> Optional[PasswordResetIntentEntity]:
        """
        Locate a password reset intent by comparing the provided challenge
        against stored hashes. Only non-consumed, non-expired intents
        are considered.
        """
        now = datetime.now(timezone.utc)

        intents = PasswordResetIntentModel.objects.filter(
            consumed=False,
            expires_at__gt=now,
        )

        for intent in intents:
            if check_password(challenge_code, intent.challenge_hash):
                return PasswordResetIntentMapper.to_entity(intent)

        return None

    # -------------------------
    # Mark consumed
    # -------------------------
    def mark_consumed(self, intent_id: UUID) -> Result[None]:
        try:
            with transaction.atomic():
                updated = PasswordResetIntentModel.objects.filter(
                    id=intent_id,
                    consumed=False,
                ).update(
                    consumed=True,
                    consumed_at=datetime.now(timezone.utc),
                )

                if updated == 0:
                    return NotOk(
                        message="password reset intent already consumed or not found",
                        static_msg="RESET_INTENT_INVALID",
                        status_code=400,
                    )

                return Ok(None)

        except Exception as e:
            return Error(
                message="failed to mark password reset intent as consumed",
                exception=e,
            )
