# apps/api_v0.py
import logging

from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

from api.utils.docs_ui import add_dark_mode_toggle
from apps.app_system.application.delivery.app_sys_controller import AppSystemController
from apps.authentication.application.delivery.auth_controller import AuthenticationController
from apps.authorization.application.delivery.authorization_controller import AuthorizationController
from apps.commentsections.application.delivery.comment_sections_controller import CommentSectionsController
from apps.feeds.application.delivery.feeds_controller import FeedsController
from apps.moderation_sys.application.delivery.moderation_controller import ModerationController
from apps.posts.application.delivery.posts_controller import PostsController
from apps.profiles.application.delivery.profiles_controller import ProfilesController
from apps.registration.application.delivery.registration_controller import RegistrationController
from apps.users.application.delivery.users_controller import UsersController


api = NinjaExtraAPI(version="v0", title="Memeinator API", docs_decorator=add_dark_mode_toggle)

api.register_controllers(
    AppSystemController,
    AuthenticationController,
    AuthorizationController,
    CommentSectionsController,
    FeedsController,
    ModerationController,
    PostsController,
    ProfilesController,
    RegistrationController,
    UsersController
)

# ------------------------------------------

# Logging exception handler at API level
logger = logging.getLogger("apps")
@api.exception_handler(Exception)
def global_exception_handler(request, exception):
    logger.exception(f"Unhandled Exception at {request.path}")
    return api.create_response(request, {"detail": "Internal Server Error"}, status=500)