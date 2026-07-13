# apps/registration/domain/usecases/user_registration_usecase.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict
from uuid import UUID, uuid7

from apps.registration.application.dtos.user_registration_response_schema import UserRegistrationResponseSchema
from apps.registration.domain.entities.registration_result_entity import RegistrationResultEntity
from apps.registration.domain.enums.registration_error_code import RegistrationErrorCode
from apps.registration.domain.iusecases.iuser_registration_usecase import IUserRegistrationUsecase
from apps.users.domain.entities.user_entity import UserEntity
from apps.users.domain.irepositories.user_repository import IUserRepository
from apps.users.infrastructure.repositories.user_repository import UserRepository
from core.results import NotOk, Ok, Result


class UserRegisterUsecase(IUserRegistrationUsecase):
    """
    Creates a user via the user repository and returns a RegistrationResultEntity.

    NOTE about passwords:
      - `password` param is interpreted as RAW password by default and will be
        hashed with Django's set_password() via the repository.
      - If your client truly sends a pre-hashed password string compatible
        with Django's `password` field, set password_is_hashed=True.
    """

    def __init__(
            self, 
            user_repo: IUserRepository = None
        ):
        self.user_repo = user_repo or UserRepository()

    def execute(
        self,
        *,
        user_name: str,
        email: str,
        raw_password: str,
    ) -> Result[UserEntity]:

        # 1) validate uniqueness (simple checks here; expand as needed)
        if self.user_repo.get_by_username(user_name) is not None:
            return NotOk(
                message="username already exists",
                static_msg=RegistrationErrorCode.USERNAME_TAKEN,
                status_code=409 # TODO: IS THIS A SECURITY RISK?
            )

        if self.user_repo.get_by_email(email) is not None:
            return NotOk(
                message="email already exists",
                static_msg=RegistrationErrorCode.EMAIL_TAKEN,
                status_code=409 # TODO: IS THIS A SECURITY RISK?
            )

        # 2) create UserEntity (attach password on the entity so repository can persist)
        #    We attach `password` attribute to the entity for convenience; repo will handle it.
        new_user = UserEntity(
            id = None, # Let django generate the UUID7
            username=user_name,
            email=email,
            is_online=False,
            is_verified=False,
            is_banned=False,
            date_joined=None,
            profile=None,
            is_soft_deleted=False,
        )

        # NOTE: password not stored in UserEntity

        # 3) persist (persisted_user has id assigned to it)
        persisted_user = self.user_repo.create(
            new_user, 
            password=raw_password,
            password_is_hashed=False
        )

        return Ok(persisted_user)
