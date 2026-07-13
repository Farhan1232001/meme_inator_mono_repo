# apps/registration/domain/orchestrations/registration_orchestration.py
from typing import Optional
from django.db import transaction
from apps.profiles.domain.entities.profile_entity import ProfileEntity
from apps.profiles.domain.usecases.icreate_user_profile_usercase import ICreateUserProfileUsecase
from apps.registration.application.dtos.user_registration_response_schema import UserRegistrationResponseSchema
from apps.registration.application.usecases.user_register_usecase import RegistrationResultEntity
from apps.registration.domain.entities.registration_intent_token_entity import RegistrationIntentTokenEntity
from apps.registration.domain.entities.registration_result_entity import RegistrationResultEntity
from apps.registration.domain.iusecases.icreate_registration_intent_token_usecase import ICreateRegistrationIntentTokenUsecase
from apps.registration.domain.iusecases.iregistration_verification_usecase import IRegistrationVerificationUsecase
from apps.registration.domain.iusecases.iuser_registration_usecase import IUserRegistrationUsecase
from apps.users.domain.entities.user_entity import UserEntity
from core.results import Error, NotOk, Ok, Result


class RegistrationOrchestration:
    """
    Coordinates registration-related usecases, specifically UserRegistrationUsecase (should be called CreateUserUsecase) and CreateUserProfileUsecase.

    Registration is a TWO step process: register_intent and register_verification
    Deregistration is a TWO step process: deregister_intent and deregister_confirmation
    """

    def __init__(
        self,
        register_user_usecase: IUserRegistrationUsecase,
        create_profile_usecase: ICreateUserProfileUsecase,
        create_registration_intent_token_usecase: ICreateRegistrationIntentTokenUsecase,
        registration_verification_usecase: IRegistrationVerificationUsecase
    ):
        self._register_user_usecase = register_user_usecase
        self._create_profile_usecase = create_profile_usecase
        self._create_registration_intent_token_usecase = create_registration_intent_token_usecase
        self._registration_verification_usecase = registration_verification_usecase

    def register_intent(
        self,
        *,
        user_name: str,
        email: str,
        raw_password: str,
        require_email_verification: bool
    ) -> Result[RegistrationResultEntity]:
        """
        Atomically creates a user and their profile.
        Returns Ok(RegistrationResultEntity) on success,
        NotOk/Error if anything fails.
        """
        try:
            # Use Django transaction.atomic so everything rolls back on failure
            with transaction.atomic():
                # 1. Create user
                user_result: Result[UserEntity] = self._register_user_usecase.execute(
                    user_name=user_name,
                    email=email,
                    raw_password=raw_password,
                )

                # ... Propagate NotOk / Error from user creation
                if isinstance(user_result, (NotOk, Error)):
                    transaction.set_rollback(True)
                    return user_result
                
                new_user = user_result.value
                
                # 2. If registration verification required, create & persist RegistrationIntentToken
                if require_email_verification:
                    intent_token_result:Result[RegistrationIntentTokenEntity] = self._create_registration_intent_token_usecase.execute(
                        user_id = new_user.id
                    )

                    if isinstance(intent_token_result, (NotOk, Error)):
                        transaction.set_rollback(True)
                        # TODO: is this ok?
                        return intent_token_result
                    
                    self._registration_verification_usecase.send_verification_email(
                        email=new_user.email,
                        intent_token=intent_token_result.value
                    )
                    

                
                # 3. Create profile for the user
                profile_result: Result[ProfileEntity] = self._create_profile_usecase.execute(user_id=new_user.id)

                # ... If profile creation failed, propagate NotOk or Error so transaction rolls back
                if isinstance(profile_result, (NotOk, Error)):
                    transaction.set_rollback(True)
                    return profile_result

                # 4. Both succeeded — attach profile to the user (and to the registration entity)
                profile_entity = profile_result.value
                new_user.profile = profile_entity

                # 5. Create RegistrationEntity with post-create hooks (verification, token generation) — left minimal
                
                registration_entity = RegistrationResultEntity(
                    user =       None       if require_email_verification else new_user,
                    profile =    None       if require_email_verification else profile_entity,
                    requires_verification = require_email_verification,    # if this is True, everything else will be null
                    tokens = None,
                )

                return Ok(registration_entity)

        except Exception as e:
            # Unexpected error — return Error with exception attached
            return Error(message="failed to register user", exception=e)


    def register_verification(self, token: str) -> Result[RegistrationResultEntity]:
        """
        Verifies a pending registration using a RegistrationIntentToken.
        """
        try:
            with transaction.atomic():

                # 1. Load registration intent token
                intent_result = self._registration_verification_usecase.get_intent_by_token(token)
                if isinstance(intent_result, (NotOk, Error)):
                    transaction.set_rollback(True)
                    return intent_result

                intent_token: RegistrationIntentTokenEntity = intent_result.value

                # 2. Validate token state (expiry / consumed)
                validation_result = self._registration_verification_usecase.validate_intent(intent_token)
                if isinstance(validation_result, (NotOk, Error)):
                    transaction.set_rollback(True)
                    return validation_result

                # 3. Mark token as consumed
                consume_result = self._registration_verification_usecase.consume_intent(intent_token)
                if isinstance(consume_result, (NotOk, Error)):
                    transaction.set_rollback(True)
                    return consume_result

                # 4. Mark user as verified
                user_result: Result[UserEntity] = self._register_user_usecase.mark_verified(
                    user_id=intent_token.user_id
                )
                if isinstance(user_result, (NotOk, Error)):
                    transaction.set_rollback(True)
                    return user_result

                verified_user = user_result.value

                # 5. Load profile
                profile_result: Result[ProfileEntity] = self._create_profile_usecase.get_by_user_id(
                    user_id=verified_user.id
                )
                if isinstance(profile_result, (NotOk, Error)):
                    transaction.set_rollback(True)
                    return profile_result

                profile = profile_result.value
                verified_user.profile = profile

                # 6. Build result entity
                result = RegistrationResultEntity(
                    user=verified_user,
                    profile=profile,
                    requires_verification=False,
                    tokens=None,
                )

                return Ok(result)

        except Exception as e:
            return Error(message="failed to verify registration", exception=e)


    def deregister_intent(self, refresh_token: str) -> Result:
        """
        Initiates a deregistration intent:
          - validates refresh token -> user_id
          - generates numeric challenge (returns entity + plain_code)
          - persists challenge entity
          - emails the plain code (frontend-bridge)
        Returns Ok("challenge sent") on success.
        """
        try:
            # Preconditions: required dependencies must be provided
            if not all([
                self._validate_refresh_token_usecase,
                self._create_deregistration_intent_usecase,
                self._deregistration_challenge_repo,
                self._deregistration_verification_usecase,
                self._user_repo,
            ]):
                return Error(message="deregistration not configured", exception=None)

            # 1) validate refresh token and obtain user_id
            validate_result = self._validate_refresh_token_usecase.execute(refresh_token)
            if isinstance(validate_result, (NotOk, Error)):
                return validate_result

            user_id = validate_result.value

            # 2) create the DeregistrationIntentChallenge entity and plain code
            create_result = self._create_deregistration_intent_usecase.execute(user_id)
            if isinstance(create_result, (NotOk, Error)):
                return create_result

            entity, plain_code = create_result.value

            # 3) persist the entity
            persist_result = self._deregistration_challenge_repo.create(entity)
            if isinstance(persist_result, (NotOk, Error)):
                return persist_result

            # 4) fetch user email
            user = self._user_repo.get_by_id(user_id)
            if user is None:
                return NotOk(message="user not found", static_msg="USER_NOT_FOUND", status_code=404)

            # 5) send email with plain numeric code (via verification usecase)
            send_result = self._deregistration_verification_usecase.send_deregistration_email(
                email=user.email,
                plain_challenge_code=plain_code
            )
            if isinstance(send_result, (NotOk, Error)):
                return send_result

            return Ok("challenge sent")

        except Exception as e:
            return Error(message="failed to initiate deregistration", exception=e)

    def deregister_confirmation(self, challenge_code: str, refresh_token: str) -> Result:
        """
        Confirms deregistration:
          - validates refresh token -> user_id
          - loads active challenge for user
          - verifies provided numeric challenge against stored hash
          - marks token consumed, soft-deletes user, revokes refresh tokens
        """
        try:
            if not all([
                self._validate_refresh_token_usecase,
                self._deregistration_challenge_repo,
                self._deregistration_verification_usecase,
                self._user_repo,
                self._refresh_token_service,
            ]):
                return Error(message="deregistration not configured", exception=None)

            with transaction.atomic():
                # 1) validate refresh token and obtain user_id
                validate_result = self._validate_refresh_token_usecase.execute(refresh_token)
                if isinstance(validate_result, (NotOk, Error)):
                    transaction.set_rollback(True)
                    return validate_result

                user_id = validate_result.value

                # 2) load active challenge for user
                intent_result = self._deregistration_challenge_repo.get_active_for_user(user_id)
                if isinstance(intent_result, (NotOk, Error)):
                    # propagate NotOk/Error (e.g., no pending deregistration)
                    transaction.set_rollback(True)
                    return intent_result

                intent_entity = intent_result.value

                # 3) verify challenge code
                verify_result = self._deregistration_verification_usecase.verify_challenge(challenge_code, intent_entity)
                if isinstance(verify_result, (NotOk, Error)):
                    transaction.set_rollback(True)
                    return verify_result

                # verify_result is Ok(user_id) on success (or similar)
                # 4) soft-delete user
                update_result = self._user_repo.update_is_soft_deleted(user_id, True)
                if isinstance(update_result, (NotOk, Error)):
                    transaction.set_rollback(True)
                    return update_result

                # 5) revoke refresh tokens for user
                revoke_result = self._refresh_token_service.revoke_all_for_user(user_id)
                if isinstance(revoke_result, (NotOk, Error)):
                    # revocation failure is important but decide policy: here we fail the whole op
                    transaction.set_rollback(True)
                    return revoke_result

                return Ok("account scheduled for deletion")

        except Exception as e:
            return Error(message="failed to confirm deregistration", exception=e)