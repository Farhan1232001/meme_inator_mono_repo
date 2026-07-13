# apps/posts/application/delivery/posts_controller.py
from typing import Optional, List, Dict, Any
from uuid import UUID

from django.http import HttpRequest
from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth

from apps.posts.application.dtos.vote_on_post_request_schema import VoteOnPostRequestSchema
from apps.posts.application.dtos.create_post_request_schema import CreatePostRequestSchema
from core.dependency_injections import di
from apps.commentsections.application.dtos.schemas import NewCommentRequestSchema
from core.results import Result
from core.dtos.results_schemas import NotOkResponseSchema, ErrorResponseSchema


@api_controller('/posts', tags=['posts'])
class PostsController:
    """
    Controller for Post-related resources. 
    Handles Post CRUD and acts as an entry point for Post-sub-resources like comments.
    """

    def __init__(self):
        # We inject orchestrations for both domains
        self.posts_orchestration = di.create_posts_orchestration()
        self.comment_orchestration = di.create_comment_sections_orchestration()

    # --- Post CRUD Operations ---

    @route.post(
        "/", 
        response={201: dict, 400: NotOkResponseSchema, 401: NotOkResponseSchema, 500: ErrorResponseSchema}, 
        auth=JWTAuth()
    )
    def create_post(self, request: HttpRequest, payload: CreatePostRequestSchema):
        """Create a new meme post."""
        result = self.posts_orchestration.create_post(
            author_id=request.user.id, 
            **payload.dict()
        )
        return Result.result_parser(
            result=result,
            ok_handler=lambda ok_value: (201, ok_value),
        )

    @route.get(
        "/{post_public_id}", 
        auth=None,
        response={200: dict, 404: NotOkResponseSchema}
    )
    def get_post(self, post_public_id: UUID):
        """Retrieve details of a single post."""
        result = self.posts_orchestration.get_post(post_public_id=post_public_id)
        return Result.result_parser(
            result=result,
            ok_handler=lambda ok_value: (200, ok_value),
        )

    @route.delete(
        "/{post_public_id}", 
        auth=JWTAuth(),
        response={204: None, 401: NotOkResponseSchema, 403: NotOkResponseSchema, 404: NotOkResponseSchema, 500: ErrorResponseSchema}
    )
    def delete_post(self, request: HttpRequest, post_public_id: UUID):
        """Delete a post (owner only)."""
        result = self.posts_orchestration.delete_post(
            post_public_id=post_public_id, 
            actor_id=request.user.id
        )
        return Result.result_parser(
            result=result,
            ok_handler=lambda _: (204, None),
        )

    # --- Post Voting ---

    @route.post(
        "/{post_public_id}/vote",
        auth=JWTAuth(),
        response={
            200: dict, 
            400: NotOkResponseSchema, 
            401: NotOkResponseSchema, 
            403: NotOkResponseSchema, 
            404: NotOkResponseSchema, 
            500: ErrorResponseSchema
        },
    )
    def vote_on_post(self, request: HttpRequest, post_public_id: UUID, payload: VoteOnPostRequestSchema):
        """Vote on a post."""
        user_id = getattr(request.user, "id", None)
        if not user_id:
            return 401, {"message": "unauthenticated", "static_msg": "UNAUTHORIZED"}

        result = self.posts_orchestration.vote_on_post(
            post_public_id=post_public_id,
            voter_user_id=user_id,
            action=payload.action,
        )

        # Return a dict with shape expected by NotOkResponseSchema on success
        return Result.result_parser(
            result=result,
            ok_handler=lambda value: (200, {"message": "ok", "static_msg": "post.vote_success"})
        )

    # --- Sub-resource: Comments (Delegated to CommentSectionsOrchestration) ---

    @route.get(
        "/{post_public_id}/comments",
        tags=["comments"],  # Keep 'comments' tag for API documentation grouping
        auth=None,
    )
    def list_post_comments(self, post_public_id: UUID, cursor: Optional[str] = None, page_size: int = 20):
        """
        List top-level comments for a post.
        Delegates logic to the CommentSections orchestration layer.
        """
        result = self.comment_orchestration.list_comments(
            post_public_id=post_public_id, 
            cursor=cursor, 
            page_size=page_size
        )

        return Result.result_parser(
            result=result,
            ok_handler=lambda ok_value: (200, ok_value),
        )

    @route.post(
        "/{post_public_id}/comments",
        tags=["comments"],
        auth=JWTAuth(),
        response={201: dict, 401: dict, 404: dict},
    )
    def add_post_comment(self, request: HttpRequest, post_public_id: UUID, new_comment_data: NewCommentRequestSchema):
        """
        Add a new comment to a post.
        Delegates logic to the CommentSections orchestration layer.
        """
        user_id = request.user.id

        if not user_id:
            return 401, {"message": "unauthenticated", "static_msg": "UNAUTHORIZED"}

        content = new_comment_data.content
        parent_comment_id = new_comment_data.parent_comment_id

        result = self.comment_orchestration.add_comment(
            post_public_id=post_public_id, 
            author_id=user_id, 
            content=content, 
            parent_comment_id=parent_comment_id
        )

        return Result.result_parser(
            result=result,
            ok_handler=lambda ok_value: (201, ok_value),
        )