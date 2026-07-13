from datetime import datetime, timezone
from uuid import UUID
from django.core.exceptions import ObjectDoesNotExist
from apps.profiles.domain.entities.profile_entity import ProfileEntity
from apps.profiles.domain.enums.profile_error_code import ProfileErrorCode
from apps.profiles.domain.usecases.icreate_user_profile_usercase import ICreateUserProfileUsecase
from apps.profiles.domain.irepositories.i_profile_repository import IProfileRepository
from core.results import Result, Ok, NotOk, Error

class CreateUserProfileUsecase(ICreateUserProfileUsecase):
    def __init__(self, profile_repo: IProfileRepository) -> None:
        self.profile_repo = profile_repo

    def execute(self, user_id: UUID) -> Result[ProfileEntity]:
        try:
            # 1. Idempotency check – repository already handles this, but we call create_profile
            #    which internally checks for existence and returns NotOk if already exists.
            return self.profile_repo.create_profile(user_id)
        except Exception as e:
            return Error(
                message="Failed to create user profile",
                static_msg=ProfileErrorCode.PROFILE_CREATION_ERROR,
                exception=e,
            )