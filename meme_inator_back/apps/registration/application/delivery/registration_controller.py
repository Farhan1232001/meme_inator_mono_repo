# apps/registration/api/controllers/registration_controller.py
from ninja_extra import ControllerBase, api_controller, route
from ninja_extra.permissions import AllowAny

from apps.registration.application.dtos.user_registration_request_schema import UserRegistrationRequestSchema
from apps.registration.application.dtos.user_registration_response_schema import UserRegistrationResponseSchema
from apps.registration.application.orchestration.registration_orchestration import RegistrationOrchestration
from apps.users.application.mapper import user_to_schema
from core.dependency_injections import di
from core.dtos.results_schemas import ErrorResponseSchema, NotOkResponseSchema
from core.results import Error, NotOk, Ok
from meme_inator_back import settings

@api_controller(
    "/registration",
    tags=["registration"],
    permissions=[AllowAny],
)
class RegistrationController(ControllerBase):

    def __init__(self):
        self._orchestration:RegistrationOrchestration = di.create_registration_orchestration()

    @route.post(
        "/register",
        response={
            201: UserRegistrationResponseSchema,
            400: NotOkResponseSchema,
            409: NotOkResponseSchema,
            500: ErrorResponseSchema,
        },
    )
    def register(self, payload: UserRegistrationRequestSchema):
        """
        Registers a new user.
        """

        result = self._orchestration.register_intent(
            user_name=payload.username,
            email=payload.email,
            raw_password=payload.raw_password,
            require_email_verification = False # TODO: Verification feature done AFTER frontend-bridge implemented in flutter
        )

        match result:
            case Ok(value=reg_entity):
                # two possible Ok cases: reg_entity.user in None since veritification is required, otherwise it's not None
                if reg_entity.user == None:
                    return 201, UserRegistrationResponseSchema(
                    user=None,
                    profile=None,
                    requires_verification=reg_entity.requires_verification,
                    tokens=None,
                )

                user_schema = user_to_schema(reg_entity.user)

                # model_dump gives a JSON-serializable dict (Pydantic v2 style)
                user_dict = user_schema.model_dump()
                profile_dict = None
                if getattr(user_schema, "profile", None):
                    profile_dict = user_schema.profile.model_dump()

                return 201, UserRegistrationResponseSchema(
                    user=user_dict,
                    profile=profile_dict,
                    requires_verification=reg_entity.requires_verification,
                    tokens=reg_entity.tokens,
                )

            case NotOk(message=msg, static_msg=static_msg, status_code=status_code):
                return status_code, NotOkResponseSchema(message=msg, static_msg=static_msg)

            case Error(message=msg, exception=exception, status_code=status_code):
                # debug mode returns detailed message, otherwise return generic vague message
                if settings.DEBUG:
                    # include message but the schema expects `code` as string
                    return status_code, ErrorResponseSchema(message=msg, static_msg=None, exception_str=str(exception))
                else:
                    return status_code, ErrorResponseSchema(message='internal server error')

            case _:
                return 500, ErrorResponseSchema(detail="unexpected result", code="INTERNAL_ERROR")
            
    # TODO: Create methods for deregistration and using the deregistration orchestration methods. 