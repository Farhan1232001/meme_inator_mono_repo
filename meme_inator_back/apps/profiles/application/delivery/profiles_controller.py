from django.http import HttpRequest
from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth
from typing import List, Optional, Union
from uuid import UUID

from apps.feeds.application.dtos.gf_page_response_schema import GfPageResponseSchema
from apps.feeds.application.dtos.sf_page_response_schema import SfPageResponseSchema
from apps.feeds.application.orchestration.feeds_orchestration import FeedsOrchestration
from apps.feeds.domain.entities.feed_filters_vo import FeedFilters
from apps.feeds.domain.entities.gf_page_request_vo import GridfeedPageRequestVo
from apps.feeds.domain.entities.sf_page_request_vo import SectionalFeedPageRequestVo
from apps.feeds.domain.enums.feed_type import GridFeedType, SectionalFeedType
from apps.profiles.application.dtos.profile_schema import ProfileDynamicSchema, ProfileSchema
from apps.profiles.application.dtos.profile_with_followship_context import ProfileWithFollowshipContext
from apps.profiles.application.orchestration.profiles_orchestration import ProfilesOrchestration
from apps.profiles.domain.entities.profile_light_entity import ProfileLightEntity
from core.dependency_injections import di 
from core.dtos.results_schemas import ErrorResponseSchema, NotOkResponseSchema
from core.results import Result, Ok, NotOk, Error
from meme_inator_back import settings


@api_controller("/profiles", tags=["profiles"])
class ProfilesController:
    def __init__(self):
        self._profiles_orchestration: ProfilesOrchestration = di.create_profiles_orchestration()
        self._feeds_orchestration: FeedsOrchestration = di.create_feeds_orchestration() 


    @route.get(
        "/profile/{profile_owner_user_id}/with_followship_context", 
        tags=['profiles'],
        permissions=None,
        auth=JWTAuth(),
        response={
            200: ProfileWithFollowshipContext,
            404: NotOkResponseSchema,
            500: ErrorResponseSchema
        },
        description="""
                    user_id = id of profile owner; 
                    viewer_user_id = id of user viewing the profile.
                    """
    )
    def get_public_profile_with_followship_context(
        self,
        request: HttpRequest,
        profile_owner_user_id: UUID, # user_id OF the profile owner
        fields: Optional[List[str]] = None,    
    ):
        """
        Get a public profile WITH followship context. user_id extracted from auth token. 
        Simply it returns ProfileSchema + is_following:bool appended to it. 
        TODO: Get rid of null values from response. Might have to make seperate endpoint dedicated to filtered queries. 
        """
        field_list = fields.split(',') if fields else None

        # 1. Get viewer_user_id from auth token if not explictly passed in. 
        viewer_user_id = request.user.id if request.user.is_authenticated else None

        # 2. Get profile with followship context. 
        result = self._profiles_orchestration.get_profile_with_followship_context(
            profile_owner_user_id, 
            viewer_user_id, 
            field_list
        )

        # 3. Parse result. 
        return Result.result_parser(
            result=result,
            ok_handler=lambda value : (200, value),
            default_error_message="internal server error"
        )

    @route.get(
            "/{username}", 
            tags=['profiles'],
            permissions=None,
            auth=None,
            response={
                200: ProfileDynamicSchema,
                404: NotOkResponseSchema,
                500: ErrorResponseSchema
            }
    )
    def get_public_profile(
        self,
        request: HttpRequest,
        username: str,
        viewer_user_id: Optional[UUID] = None,
        fields: Optional[str] = None, 
    ):
        """
        Get a public profile by username.
        TODO: Get rid of null values from response. Might have to make seperate endpoint dedicated to filtered queries. 
        """
        field_list = fields.split(',') if fields else None
        result = self._profiles_orchestration.get_public_profile(username, viewer_user_id, field_list)

        return Result.result_parser(
            result=result,
            # if result ProfileLight return tuple, otherwise return other tuple
            ok_handler=lambda value : (200, value),
            default_error_message="internal server error"
        )


    @route.get(
        "/me", 
        tags=['profiles'],
        permissions=None,
        auth=JWTAuth(),
        response={
            200: ProfileDynamicSchema, 
            401: NotOkResponseSchema, 
            404: NotOkResponseSchema, 
            500: ErrorResponseSchema
        }, 
    )
    def get_my_profile(self, request: HttpRequest, viewer_user_id: Optional[UUID] = None):
        """Get the authenticated user's own profile."""
        user_id = request.user.id  # Assuming JWT sets request.user

        result = self._profiles_orchestration.get_my_profile(user_id, viewer_user_id)
        return Result.result_parser(
            result=result,
            # if result ProfileLight return tuple, otherwise return other tuple
            ok_handler=lambda value : (200, value),
            default_error_message="internal server error"
        )
    

    @route.post(
        "/me", 
        tags=['profiles'],
        permissions=None,
        auth=JWTAuth(),
        response={
            201: ProfileSchema, 
            409: NotOkResponseSchema, 
            500: ErrorResponseSchema
        },
        deprecated=True,  # This marks it as deprecated in OpenAPI/Swagger docs
        description="[DEPRECATED] Profile is automatically created when user is created. This endpoint will be removed."
    )
    def create_profile(self, request: HttpRequest):
        """Create a profile for the authenticated user.
        TODO: Remove this endpoint, profile created whenever a user is created. 
        """
        raise NotImplementedError("This method is deprecated and will be removed. Profile is automatically created when user is created.")

    @route.patch(
        "/me",  
        tags=['profiles'],
        permissions=None,
        auth=JWTAuth(),
        response={
            200: ProfileSchema, 
            400: NotOkResponseSchema, 
            404: NotOkResponseSchema, 
            500: ErrorResponseSchema
        },
    )
    def patch_my_profile(self, request: HttpRequest, payload: dict):
        """Partially update own profile."""
        user_id = request.user.id
        result = self._profiles_orchestration.patch_my_profile(user_id, payload)
        return Result.result_parser(
            result=result,
            ok_handler=lambda value: (200, value),
            default_error_message="internal server error"
        )

    @route.put(
        "/me", 
        tags=['profiles'],
        permissions=None,
        auth=JWTAuth(),
        response={
            200: ProfileSchema, 
            400: NotOkResponseSchema, 
            404: NotOkResponseSchema, 
            500: ErrorResponseSchema}, 
    )
    def replace_my_profile(self, request: HttpRequest, payload: dict):
        """Fully replace own profile."""
        user_id = request.user.id
        result = self._profiles_orchestration.replace_my_profile(user_id, payload)
        return Result.result_parser(
            result=result,
            ok_handler=lambda value: (200, value),
            default_error_message="internal server error"
        )

    # TODO: IS this redundant?
    @route.patch(
        "/me/counters", 
        tags=['profiles'],
        permissions=None,
        auth=JWTAuth(),
        response={
            200: ProfileSchema, 
            400: NotOkResponseSchema, 
            404: NotOkResponseSchema, 
            500: ErrorResponseSchema},
        )
    def update_counters(self, request: HttpRequest, increments: dict):
        """Update profile counters (e.g., followers)."""
        user_id = request.user.id
        result = self._profiles_orchestration.update_counters(user_id, increments)
        return Result.result_parser(
            result=result,
            ok_handler=lambda value: (200, value),
            default_error_message="internal server error"
        )

    @route.post(
        "/me/syncMedia", 
        tags=['profiles'],
        permissions=None,
        auth=JWTAuth(),
        response={
            200: ProfileSchema, 
            400: NotOkResponseSchema, 
            404: NotOkResponseSchema, 
            500: ErrorResponseSchema}
        )
    def sync_media(self, request: HttpRequest, media_payload: dict):
        """Sync media URLs after upload."""
        user_id = request.user.id
        result = self._profiles_orchestration.sync_media(user_id, media_payload)
        return Result.result_parser(
            result=result,
            ok_handler=lambda value: (200, value),
            default_error_message="internal server error"
        )


    @route.get(
        "/me/images", 
        tags=['profiles'],
        permissions=None,
        auth=JWTAuth(),
        response={
            200: dict, 
            404: NotOkResponseSchema, 
            500: ErrorResponseSchema}
        )
    def get_profile_image_urls(self, request: HttpRequest):
        """Get image URLs for own profile."""
        user_id = request.user.id
        result = self._profiles_orchestration.get_profile_image_urls(user_id)
        return Result.result_parser(
            result=result,
            ok_handler=lambda value: (200, value),
            default_error_message="internal server error"
        )

    @route.get(
        "/{username}/posts/grid",
        tags=['profiles'],
        permissions=None,
        auth=None,
        response={
            200: GfPageResponseSchema,
            400: NotOkResponseSchema,
            404: NotOkResponseSchema,
            500: ErrorResponseSchema
        }
    )
    def get_profile_posts_grid(
        self,
        request: HttpRequest,
        username: str,
        cursor: Optional[str] = None,
        requesting_user_id: Optional[str] = None,
        page_size: int = 10,
    ):
        # Build feed request with author_username filter
        feed_request = GridfeedPageRequestVo(
            feed_type=GridFeedType.USER_PROFILE,
            cursor=cursor,
            page_size=page_size,
            requesting_user_id=requesting_user_id,
            filters=FeedFilters(author_username=username)
        )

        result = self._feeds_orchestration.get_gridfeed_page(feed_request)
        return Result.result_parser(
            result=result,
            ok_handler=lambda value: (200, value),
            default_error_message="internal server error"
        )
    
    @route.get(
        "/{username}/posts/sectional",
        tags=['profiles'],
        permissions=None,
        auth=None,
        response={
            200: SfPageResponseSchema,
            404: NotOkResponseSchema,
            500: ErrorResponseSchema
        }
    )
    def get_profile_posts_sectional(
        self,
        request: HttpRequest,
        username: str,
        duration_unit: str,
        duration_window_size: int = 3,
        cursor: Optional[str] = None,
        requesting_user_id: Optional[str] = None,
    ):

        # 1. Build sectional feed request with author_id filter
        feed_request = SectionalFeedPageRequestVo(
            feed_type=SectionalFeedType.USER_PROFILE,
            duration_unit=duration_unit,
            duration_window_size=duration_window_size,
            cursor=cursor,
            requesting_user_id=requesting_user_id,
            filters=FeedFilters(author_username=username)
        )

        # 2. Execute and return
        result = self._feeds_orchestration.get_sectional_feed_page(feed_request)
        return Result.result_parser(
            result=result,
            ok_handler=lambda value: (200, value),
            default_error_message="internal server error"
        )