# apps/feeds/controllers.py
from django.http import HttpRequest
from ninja_extra import api_controller, route
from typing import Optional
from apps.feeds.application.dtos.gf_page_response_schema import GfPageResponseSchema
from apps.feeds.application.dtos.sf_page_response_schema import SfPageResponseSchema
from apps.feeds.application.mapper import map_sf_page_response_vo_to_schema
from apps.feeds.domain.configurations.configs import get_feed_config
from apps.feeds.domain.entities.feed_filters_vo import FeedFilters
from apps.feeds.domain.entities.gf_page_request_vo import GridfeedPageRequestVo
from apps.feeds.domain.entities.gf_page_response_vo import GridfeedPageResponseVo
from apps.feeds.application.orchestration.feeds_orchestration import FeedsOrchestration
from apps.feeds.domain.entities.sf_page_request_vo import SectionalFeedPageRequestVo
from apps.feeds.domain.enums.feed_type import GridFeedType
from core.dtos.results_schemas import ErrorResponseSchema, NotOkResponseSchema
from core.results import Error, NotOk, Ok, Result
from ninja_extra.permissions import AllowAny
from ninja_jwt.authentication import JWTAuth
from meme_inator_back import settings
from core.dependency_injections import di
from ninja_jwt.exceptions import AuthenticationFailed


@api_controller("/feeds")
class FeedsController:
    """
    Django-Ninja controller exposing feed endpoints with query parameters.

    Authentication is handled conditionally based on feed_type configuration.
    - Public feed types: recent, randomized, videos_only, images_only, most_commented, user_profile
    - Private feed types: friends, following, subscriber_likes, user_liked_posts, commented_feeds
    """

    def __init__(self):
        self._feeds_orchestration: FeedsOrchestration = di.create_feeds_orchestration()

    @route.get(
        '/grid_feed',
        tags=['feeds'],
        auth=None,  # No global auth - authentication handled conditionally
        permissions=[AllowAny],  # Allow any to bypass permission checks
        response={
            200: GfPageResponseSchema,
            400: NotOkResponseSchema,
            401: NotOkResponseSchema,
            404: NotOkResponseSchema,
            500: ErrorResponseSchema
        }
    )
    def get_grid_feed(
        self, 
        request: HttpRequest,
        feed_type: str,
        page_size: Optional[int] = 10,
        cursor: Optional[str] = None,
        author_username: Optional[str] = None,
    ) -> GfPageResponseSchema:
        """
        Get grid feed with conditional authentication.
        
        Authentication is determined by the feed_type:
        - Public feed types (recent, randomized, videos_only, images_only, most_commented, user_profile): No auth required
        - Private feed types (friends, following, subscriber_likes, user_liked_posts, commented_feeds): JWT required
        
        Query Parameters:
        - feed_type: str (required)
        - page_size: int (optional, default=10)
        - cursor: str (optional)
        - author_username: str (optional) - filter posts by author's username
        """
        # Extract authenticated user ID if present (JWTAuth would set this, but we use conditional logic)
        # Since we use auth=None, request.user might not be set by JWTAuth middleware
        # We need to manually attempt authentication here
        requesting_user_id = self._get_authenticated_user_id(request)
        
        # Validate feed_type and get config
        try:
            config = get_feed_config(GridFeedType(feed_type))
        except ValueError:
            return 400, NotOkResponseSchema(
                message=f"Unsupported feed_type: '{feed_type}' - possible types are: {GridFeedType.get_gridfeed_values()}",
                static_msg="INVALID_FEED_TYPE",
                status_code=400
            )
        
        # Check if authentication is required for this feed type
        if config["auth_required"] and not requesting_user_id:
            return 401, NotOkResponseSchema(
                message="Authentication required for this feed type. Please provide a valid JWT token.",
                static_msg="UNAUTHORIZED",
                status_code=401
            )
        
        # Build optional filters
        filters = FeedFilters(author_username=author_username) if author_username else None
        
        # Create request value object
        gf_page_request_vo = GridfeedPageRequestVo(
            feed_type=feed_type,
            cursor=cursor,
            page_size=page_size,
            requesting_user_id=requesting_user_id,
            filters=filters
        )
        
        # Get response from orchestration
        gf_pg_response_vo_result: Result[GridfeedPageResponseVo] = (
            self._feeds_orchestration.get_gridfeed_page(request_vo=gf_page_request_vo)
        )
        
        # Convert result to HTTP response
        return self._handle_grid_feed_result(gf_pg_response_vo_result)

    @route.get(
        '/sectional_feed',
        tags=['feeds'],
        auth=None,  # No global auth - handled conditionally
        permissions=[AllowAny],
        response={
            200: SfPageResponseSchema,
            400: NotOkResponseSchema,
            401: NotOkResponseSchema,
            404: NotOkResponseSchema,
            500: ErrorResponseSchema
        }
    )
    def get_sectional_feed(
        self, 
        request: HttpRequest,
        feed_type: str,
        duration_unit: str,
        duration_window_size: Optional[int] = 3,
        cursor: Optional[str] = None,
        author_username: Optional[str] = None,
    ) -> SfPageResponseSchema:
        """
        Get sectional feed with conditional authentication.
        
        Authentication is determined by the feed_type configuration.
        Some sectional feed types may require authentication (e.g., user_profile).
        
        Query Parameters:
        - feed_type: str (required)
        - duration_unit: str (required)
        - duration_window_size: int (optional, default=3)
        - cursor: str (optional)
        - author_username: str (optional) - filter posts by author's username
        """
        # Extract authenticated user ID if present
        requesting_user_id = self._get_authenticated_user_id(request)
        
        # Build optional filters
        filters = FeedFilters(author_username=author_username) if author_username else None
        
        # Create request value object
        sf_pg_request_vo = SectionalFeedPageRequestVo(
            feed_type=feed_type,
            duration_unit=duration_unit,
            duration_window_size=duration_window_size,
            cursor=cursor,
            filters=filters,
            requesting_user_id=requesting_user_id
        )
        
        # Get response from orchestration
        sf_pg_response_result: Result = self._feeds_orchestration.get_sectional_feed_page(
            request_vo=sf_pg_request_vo,
        )
        
        # Convert result to HTTP response
        return self._handle_sectional_feed_result(sf_pg_response_result)

    # --------------------------------------------------------------------------
    # Private helper methods
    # --------------------------------------------------------------------------

    def _get_authenticated_user_id(self, request: HttpRequest) -> Optional[str]:
        """
        Attempt to authenticate the request and return the user ID if valid.
        
        Since we use auth=None, we manually extract and validate the JWT token.
        
        Returns:
            user_id (str) if authenticated, None otherwise
        """
        try:
            # Get the Authorization header
            auth_header = request.headers.get('Authorization', '')
            if not auth_header: return None
            
            # Extract token from "Bearer <token>" format
            parts = auth_header.split()
            if len(parts) != 2 or parts[0] != 'Bearer': return None
            
            token = parts[1]
            
            # Authenticate with the token
            # TODO: Is creating JWTAuth instance everytime auth for request needed inefficient?
            jwt_auth = JWTAuth()
            user = jwt_auth.authenticate(request, token)
            if user and hasattr(user, 'id'):
                return str(user.id)
            elif user and hasattr(user, 'pk'):
                return str(user.pk)
            
            return None
            
        except AuthenticationFailed as e: 
            return None
        except Exception as e:
            # Any other error - just return None
            return None

    def _handle_grid_feed_result(
        self, result: Result[GridfeedPageResponseVo]
    ) -> GfPageResponseSchema:
        """Convert a grid feed result to an HTTP response tuple."""
        match result:
            case Ok(value=gf_pg_response):
                return 200, GfPageResponseSchema(
                    next_cursor=gf_pg_response.next_cursor,
                    results=gf_pg_response.results
                )
            case NotOk(message=msg, static_msg=static_msg, status_code=status_code):
                return status_code, NotOkResponseSchema(
                    message=msg,
                    static_msg=static_msg,
                    status_code=status_code
                )
            case Error(message=message, static_msg=static_msg, exception=exception, status_code=status_code):
                if settings.DEBUG:
                    return status_code, ErrorResponseSchema(
                        message=message,
                        static_msg=static_msg,
                        exception_str=str(exception)
                    )
                else:
                    return status_code, ErrorResponseSchema(message='internal server error')
            case _:
                return 500, ErrorResponseSchema(detail="unexpected result", code="INTERNAL_ERROR")

    def _handle_sectional_feed_result(
        self, result: Result
    ) -> SfPageResponseSchema:
        """Convert a sectional feed result to an HTTP response tuple."""
        match result:
            case Ok(value=sf_pg_response):
                return map_sf_page_response_vo_to_schema(sf_pg_response)
            case NotOk(message=msg, static_msg=static_msg, status_code=status_code):
                return status_code, NotOkResponseSchema(message=msg, static_msg=static_msg)
            case Error(message=msg, exception=exception, status_code=status_code):
                if settings.DEBUG:
                    return status_code, ErrorResponseSchema(
                        message=msg,
                        static_msg=None,
                        exception_str=exception.__str__()
                    )
                else:
                    return status_code, ErrorResponseSchema(message='internal server error')
            case _:
                return 500, ErrorResponseSchema(detail="unexpected result", code="INTERNAL_ERROR")

# # apps/feeds/controllers.py
# from django.http import HttpRequest
# from ninja_extra import api_controller, route
# from typing import Optional
# from apps.feeds.application.dtos.gf_page_request_schema import GfPageRequestSchema
# from apps.feeds.application.dtos.gf_page_response_schema import GfPageResponseSchema
# from apps.feeds.application.dtos.sf_page_request_schema import SfPageRequestSchema
# from apps.feeds.application.dtos.sf_page_response_schema import SfPageResponseSchema
# from apps.feeds.application.mapper import map_sf_page_response_vo_to_schema
# from apps.feeds.domain.configurations.configs import get_feed_config
# from apps.feeds.domain.entities.feed_filters_vo import FeedFilters
# from apps.feeds.domain.entities.gf_page_request_vo import GridfeedPageRequestVo
# from apps.feeds.domain.entities.gf_page_response_vo import GridfeedPageResponseVo
# from apps.feeds.application.orchestration.feeds_orchestration import FeedsOrchestration
# from apps.feeds.domain.entities.sf_page_request_vo import SectionalFeedPageRequestVo
# from apps.feeds.domain.enums.feed_type import GridFeedType
# from core.dtos.results_schemas import ErrorResponseSchema, NotOkResponseSchema
# from core.results import Error, NotOk, Ok, Result
# from ninja_extra.permissions import AllowAny
# from ninja_jwt.authentication import JWTAuth
# from meme_inator_back import settings
# from core.dependency_injections import di

# @api_controller("/feeds")
# class FeedsController:
#     """
#     Django-Ninja controller exposing feed endpoints with query parameters.

#     Example: GET /api/v0/feeds/grid_feed?feed_type=...&cursor=...&page_size=...
#     """

#     def __init__(self):
#         self._feeds_orchestration:FeedsOrchestration = di.create_feeds_orchestration()
    

#     @route.get(
#         '/grid_feed',
#         tags=['feeds'],
#         permissions=None,
#         auth=None, # No global auth - handled conditionally
#         response={
#             200: GfPageResponseSchema,
#             400: NotOkResponseSchema,
#             401: NotOkResponseSchema,
#             404: NotOkResponseSchema,
#             500: ErrorResponseSchema
#         }
#     )
#     def get_grid_feed(
#         self, 
#         request: HttpRequest,
#         feed_type: str,
#         page_size: Optional[int] = 10,
#         cursor: Optional[str] = None,
#         requesting_user_id: Optional[str] = None,
#         author_username: Optional[str] = None,
#     ) -> GfPageResponseSchema:
#         """
#         Get grid feed with query parameters.
#         Query Parameters:
#         - feed_type: str (required)
#         - page_size: int (optional, default=10)
#         - cursor: str (optional)
#         - requesting_user_id: str (optional)
#         - author_username: str (optional) - filter posts by author's username
#         """

#         # 0. Get authenticated user ID from request (if any)
#         # ... Check if feed_type requires authentication
#         requesting_user_id = request.user.id if request.user.is_authenticated else None
#         breakpoint()
#         # ... get feed config enum
#         try:
#             config = get_feed_config(GridFeedType(feed_type))
#         except ValueError:
#             return 400, NotOkResponseSchema(
#                 message=f"Unsupported feed_type: {feed_type}",
#                 static_msg="INVALID_FEED_TYPE",
#                 status_code=400
#             )
#         # ... check config if auth is required. 
#         if config["auth_required"] and not requesting_user_id:
#             return 401, NotOkResponseSchema(
#                 message="Authentication required",
#                 static_msg="UNAUTHORIZED",
#                 status_code=401
#             )


#         # 1. Build filters if author_username is provided
#         filters = FeedFilters(author_username=author_username) if author_username else None

#         # 2. Convert query parameters to request value object
#         gf_page_request_vo = GridfeedPageRequestVo(
#             feed_type=feed_type,
#             cursor=cursor,
#             page_size=page_size,
#             requesting_user_id=requesting_user_id,
#             filters=filters
#         )

#         # 3. Get response result
#         gf_pg_response_vo_result:Result[GridfeedPageResponseVo] = self._feeds_orchestration.get_gridfeed_page(
#             request_vo=gf_page_request_vo
#         )

#         # 4. Is result Ok? NotOk? Error? Check Result then convert val object to schema
#         match gf_pg_response_vo_result:
#             case Ok(value=gf_pg_response):
#                 return 200, GfPageResponseSchema(
#                     next_cursor=gf_pg_response.next_cursor,
#                     results=gf_pg_response.results
#                 )
#             case NotOk(message=msg, status_msg=status_msg, status_code=status_code):
#                 return status_code, NotOkResponseSchema(
#                     message=msg, 
#                     status_msg=status_msg, 
#                     static_code=status_code
#                 )
#             case Error(message=message, static_msg=static_msg, exception=exception, status_code=status_code):
#                 # debug mode returns detailed message, otherwise return generic vague message
#                 if settings.DEBUG:
#                     return status_code, ErrorResponseSchema(
#                         message=message, 
#                         static_msg=static_msg, 
#                         exception_str=str(exception)
#                     )
#                 else:
#                     return status_code, ErrorResponseSchema(message='internal server error')

#             case _:
#                 return 500, ErrorResponseSchema(detail="unexpected result", code="INTERNAL_ERROR")


#     @route.get(
#         '/sectional_feed',
#         tags=['feeds'],
#         permissions=None,
#         auth=None,
#         response={
#             200: SfPageResponseSchema,
#             400: NotOkResponseSchema,
#             401: NotOkResponseSchema,
#             404: NotOkResponseSchema,
#             500: ErrorResponseSchema
#         }
#     )
#     def get_sectional_feed(
#         self, 
#         request: HttpRequest,
#         feed_type: str,
#         duration_unit: str,
#         duration_window_size: Optional[int] = 3,
#         cursor: Optional[str] = None,
#         author_username: Optional[str] = None,
#     ) -> SfPageResponseSchema:
#         """
#         Get sectional feed with query parameters.
#         Query Parameters:
#         - feed_type: str (required)
#         - duration_unit: str (required)
#         - duration_window_size: int (optional, default=3)
#         - cursor: str (optional)
#         """
#         # 0. init Filters
#         filters = None
#         if author_username:
#             filters = FeedFilters(author_username=author_username)

#         # 1. Convert query parameters to value object
#         sf_pg_request_vo = SectionalFeedPageRequestVo(
#             feed_type=feed_type,
#             duration_unit=duration_unit,
#             duration_window_size=duration_window_size,
#             cursor=cursor,
#             filters=filters
#         )

#         # 2. Get response result using request vo from above
#         sf_pg_response_result: Result[SectionalFeedPageRequestVo] = self._feeds_orchestration.get_sectional_feed_page(
#             request_vo=sf_pg_request_vo,
#         )

#         # 3. Check Results, convert to corresponding schema
#         match sf_pg_response_result:
#             case Ok(value=sf_pg_response):
#                 return map_sf_page_response_vo_to_schema(sf_pg_response)
            
#             case NotOk(message=msg, static_msg=static_msg, status_code=status_code):
#                 return status_code, NotOkResponseSchema(message=msg, static_msg=static_msg)

#             case Error(message=msg, exception=exception, status_code=status_code):
#                 # debug mode returns detailed message, otherwise return generic vague message
#                 if settings.DEBUG:
#                     # include message but the schema expects `code` as string
#                     return status_code, ErrorResponseSchema(message=msg, static_msg=None, exception_str=exception.__str__())
#                 else:
#                     return status_code, ErrorResponseSchema(message='internal server error')

#             case _:
#                 return 500, ErrorResponseSchema(detail="unexpected result", code="INTERNAL_ERROR")
            



# code with private and public endpoints
# # apps/feeds/controllers.py
# from django.http import HttpRequest
# from ninja_extra import api_controller, route
# from typing import Optional
# from apps.feeds.application.dtos.gf_page_request_schema import GfPageRequestSchema
# from apps.feeds.application.dtos.gf_page_response_schema import GfPageResponseSchema
# from apps.feeds.application.dtos.sf_page_request_schema import SfPageRequestSchema
# from apps.feeds.application.dtos.sf_page_response_schema import SfPageResponseSchema
# from apps.feeds.application.mapper import map_sf_page_response_vo_to_schema
# from apps.feeds.domain.configurations.configs import get_feed_config
# from apps.feeds.domain.entities.feed_filters_vo import FeedFilters
# from apps.feeds.domain.entities.gf_page_request_vo import GridfeedPageRequestVo
# from apps.feeds.domain.entities.gf_page_response_vo import GridfeedPageResponseVo
# from apps.feeds.application.orchestration.feeds_orchestration import FeedsOrchestration
# from apps.feeds.domain.entities.sf_page_request_vo import SectionalFeedPageRequestVo
# from apps.feeds.domain.enums.feed_type import GridFeedType
# from core.dtos.results_schemas import ErrorResponseSchema, NotOkResponseSchema
# from core.results import Error, NotOk, Ok, Result
# from ninja_extra.permissions import AllowAny
# from ninja_jwt.authentication import JWTAuth
# from meme_inator_back import settings
# from core.dependency_injections import di


# @api_controller("/feeds")
# class FeedsController:
#     """
#     Django-Ninja controller exposing feed endpoints with query parameters.

#     Example: GET /api/v0/feeds/grid_feed/public?feed_type=...&cursor=...&page_size=...
#     """

#     def __init__(self):
#         self._feeds_orchestration: FeedsOrchestration = di.create_feeds_orchestration()

#     # --------------------------------------------------------------------------
#     # Grid feed public and private endpoints
#     # --------------------------------------------------------------------------

#     @route.get(
#         '/grid_feed/public',
#         tags=['feeds'],
#         auth=None,
#         permissions=[AllowAny],
#         response={
#             200: GfPageResponseSchema,
#             400: NotOkResponseSchema,
#             401: NotOkResponseSchema,
#             404: NotOkResponseSchema,
#             500: ErrorResponseSchema
#         }
#     )
#     def get_grid_feed_public(
#         self,
#         request: HttpRequest,
#         feed_type: str,
#         page_size: Optional[int] = 10,
#         cursor: Optional[str] = None,
#         author_username: Optional[str] = None,
#         requesting_user_id: Optional[str] = None
#     ) -> GfPageResponseSchema:
#         """
#         Public grid feed endpoint - no authentication required.
#         Query parameters:
#         - feed_type: str (required)
#         - page_size: int (optional, default=10)
#         - cursor: str (optional)
#         - author_username: str (optional) - filter posts by author's username
#         """
#         return self._get_grid_feed_page(
#             request=request,
#             feed_type=feed_type,
#             page_size=page_size,
#             cursor=cursor,
#             author_username=author_username,
#             requesting_user_id=None  # public always uses None
#         )

#     @route.get(
#         '/grid_feed/private',
#         tags=['feeds'],
#         auth=JWTAuth(),  # enforce authentication
#         response={
#             200: GfPageResponseSchema,
#             400: NotOkResponseSchema,
#             401: NotOkResponseSchema,
#             404: NotOkResponseSchema,
#             500: ErrorResponseSchema
#         }
#     )
#     def get_grid_feed_private(
#         self,
#         request: HttpRequest,
#         feed_type: str,
#         page_size: Optional[int] = 10,
#         cursor: Optional[str] = None,
#         author_username: Optional[str] = None,
#     ) -> GfPageResponseSchema:
#         """
#         Private grid feed endpoint - requires a valid JWT token.
#         The requesting user ID is taken from the authenticated user.
#         Query parameters:
#         - feed_type: str (required)
#         - page_size: int (optional, default=10)
#         - cursor: str (optional)
#         - author_username: str (optional) - filter posts by author's username
#         """
#         # request.user is guaranteed to be set by JWTAuth
#         return self._get_grid_feed_page(
#             request=request,
#             feed_type=feed_type,
#             page_size=page_size,
#             cursor=cursor,
#             author_username=author_username,
#             requesting_user_id=request.user.id
#         )

#     # --------------------------------------------------------------------------
#     # Sectional feed public and private endpoints
#     # --------------------------------------------------------------------------

#     @route.get(
#         '/sectional_feed/public',
#         tags=['feeds'],
#         auth=None,
#         permissions=[AllowAny],
#         response={
#             200: SfPageResponseSchema,
#             400: NotOkResponseSchema,
#             401: NotOkResponseSchema,
#             404: NotOkResponseSchema,
#             500: ErrorResponseSchema
#         }
#     )
#     def get_sectional_feed_public(
#         self,
#         request: HttpRequest,
#         feed_type: str,
#         duration_unit: str,
#         duration_window_size: Optional[int] = 3,
#         cursor: Optional[str] = None,
#         author_username: Optional[str] = None,
#     ) -> SfPageResponseSchema:
#         """
#         Public sectional feed endpoint - no authentication required.
#         Query parameters:
#         - feed_type: str (required)
#         - duration_unit: str (required)
#         - duration_window_size: int (optional, default=3)
#         - cursor: str (optional)
#         - author_username: str (optional) - filter posts by author's username
#         """
#         return self._get_sectional_feed_page(
#             request=request,
#             feed_type=feed_type,
#             duration_unit=duration_unit,
#             duration_window_size=duration_window_size,
#             cursor=cursor,
#             author_username=author_username,
#             requesting_user_id=None  # public always uses None
#         )

#     @route.get(
#         '/sectional_feed/private',
#         tags=['feeds'],
#         auth=[JWTAuth()],
#         response={
#             200: SfPageResponseSchema,
#             400: NotOkResponseSchema,
#             401: NotOkResponseSchema,
#             404: NotOkResponseSchema,
#             500: ErrorResponseSchema
#         }
#     )
#     def get_sectional_feed_private(
#         self,
#         request: HttpRequest,
#         feed_type: str,
#         duration_unit: str,
#         duration_window_size: Optional[int] = 3,
#         cursor: Optional[str] = None,
#         author_username: Optional[str] = None,
#     ) -> SfPageResponseSchema:
#         """
#         Private sectional feed endpoint - requires a valid JWT token.
#         The requesting user ID is taken from the authenticated user.
#         Query parameters:
#         - feed_type: str (required)
#         - duration_unit: str (required)
#         - duration_window_size: int (optional, default=3)
#         - cursor: str (optional)
#         - author_username: str (optional) - filter posts by author's username
#         """
#         return self._get_sectional_feed_page(
#             request=request,
#             feed_type=feed_type,
#             duration_unit=duration_unit,
#             duration_window_size=duration_window_size,
#             cursor=cursor,
#             author_username=author_username,
#             requesting_user_id=request.user.id
#         )

#     # --------------------------------------------------------------------------
#     # Private helper methods that contain the core logic
#     # --------------------------------------------------------------------------

#     def _get_grid_feed_page(
#         self,
#         request: HttpRequest,
#         feed_type: str,
#         page_size: int,
#         cursor: Optional[str],
#         author_username: Optional[str],
#         requesting_user_id: Optional[str],
#     ) -> GfPageResponseSchema:
#         """
#         Shared logic for retrieving a grid feed page.
#         Returns the response tuple (status_code, schema) directly.
#         """
#         # 1. Validate feed_type
#         try:
#             config = get_feed_config(GridFeedType(feed_type))
#         except ValueError:
#             return 400, NotOkResponseSchema(
#                 message=f"Unsupported feed_type: '{feed_type}' - possible types are: {GridFeedType.get_gridfeed_values()}",
#                 static_msg="INVALID_FEED_TYPE",
#                 status_code=400
#             )

#         # 2. Check if authentication is required for this feed type
#         if config["auth_required"] and not requesting_user_id:
#             return 401, NotOkResponseSchema(
#                 message="Authentication required",
#                 static_msg="UNAUTHORIZED",
#                 status_code=401
#             )

#         # 3. Build optional filters
#         filters = FeedFilters(author_username=author_username) if author_username else None

#         # 4. Create request value object
#         gf_page_request_vo = GridfeedPageRequestVo(
#             feed_type=feed_type,
#             cursor=cursor,
#             page_size=page_size,
#             requesting_user_id=requesting_user_id,
#             filters=filters
#         )

#         # 5. Get result from orchestration
#         gf_pg_response_vo_result: Result[GridfeedPageResponseVo] = (
#             self._feeds_orchestration.get_gridfeed_page(request_vo=gf_page_request_vo)
#         )

#         # 6. Convert result to HTTP response
#         return self._handle_grid_feed_result(gf_pg_response_vo_result)

#     def _get_sectional_feed_page(
#         self,
#         request: HttpRequest,
#         feed_type: str,
#         duration_unit: str,
#         duration_window_size: int,
#         cursor: Optional[str],
#         author_username: Optional[str],
#         requesting_user_id: Optional[str],
#     ) -> SfPageResponseSchema:
#         """
#         Shared logic for retrieving a sectional feed page.
#         Returns the response tuple (status_code, schema) directly.
#         """
#         # 1. Build optional filters
#         filters = FeedFilters(author_username=author_username) if author_username else None

#         # 2. Create request value object
#         sf_pg_request_vo = SectionalFeedPageRequestVo(
#             feed_type=feed_type,
#             duration_unit=duration_unit,
#             duration_window_size=duration_window_size,
#             cursor=cursor,
#             filters=filters,
#             requesting_user_id=requesting_user_id  # Note: may need to be added to the VO if not present
#         )

#         # 3. Get result from orchestration
#         sf_pg_response_result: Result = self._feeds_orchestration.get_sectional_feed_page(
#             request_vo=sf_pg_request_vo,
#         )

#         # 4. Convert result to HTTP response
#         return self._handle_sectional_feed_result(sf_pg_response_result)

#     # --------------------------------------------------------------------------
#     # Result handling helpers
#     # --------------------------------------------------------------------------

#     def _handle_grid_feed_result(
#         self, result: Result[GridfeedPageResponseVo]
#     ) -> GfPageResponseSchema:
#         """Convert a grid feed result to an HTTP response tuple."""
#         match result:
#             case Ok(value=gf_pg_response):
#                 return 200, GfPageResponseSchema(
#                     next_cursor=gf_pg_response.next_cursor,
#                     results=gf_pg_response.results
#                 )
#             case NotOk(message=msg, static_msg=static_msg, status_code=status_code):
#                 return status_code, NotOkResponseSchema(
#                     message=msg,
#                     static_msg=static_msg,
#                     status_code=status_code
#                 )
#             case Error(message=message, static_msg=static_msg, exception=exception, status_code=status_code):
#                 if settings.DEBUG:
#                     return status_code, ErrorResponseSchema(
#                         message=message,
#                         static_msg=static_msg,
#                         exception_str=str(exception)
#                     )
#                 else:
#                     return status_code, ErrorResponseSchema(message='internal server error')
#             case _:
#                 return 500, ErrorResponseSchema(detail="unexpected result", code="INTERNAL_ERROR")

#     def _handle_sectional_feed_result(
#         self, result: Result
#     ) -> SfPageResponseSchema:
#         """Convert a sectional feed result to an HTTP response tuple."""
#         match result:
#             case Ok(value=sf_pg_response):
#                 return map_sf_page_response_vo_to_schema(sf_pg_response)
#             case NotOk(message=msg, static_msg=static_msg, status_code=status_code):
#                 return status_code, NotOkResponseSchema(message=msg, static_msg=static_msg)
#             case Error(message=msg, exception=exception, status_code=status_code):
#                 if settings.DEBUG:
#                     return status_code, ErrorResponseSchema(
#                         message=msg,
#                         static_msg=None,
#                         exception_str=exception.__str__()
#                     )
#                 else:
#                     return status_code, ErrorResponseSchema(message='internal server error')
#             case _:
#                 return 500, ErrorResponseSchema(detail="unexpected result", code="INTERNAL_ERROR")