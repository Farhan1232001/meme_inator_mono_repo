# apps/commentsections/application/delivery/comment_sections_controller.py
from typing import Optional, List
from uuid import UUID
from django.http import HttpRequest
from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth

from apps.commentsections.application.orchestration.comment_sections_orchestration import CommentSectionsOrchestration
from core.dependency_injections import di
from core.dtos.results_schemas import ErrorResponseSchema, NotOkResponseSchema
from core.results import Result

# Import our new Response Schemas
from apps.commentsections.application.dtos.schemas import (
    NewCommentRequestSchema, 
    UpdateCommentRequestSchema, 
    VoteOnCommentRequestSchema,
    CommentResponseSchema,
    CommentThreadResponseSchema,
)

@api_controller('/comments', tags=['comments'])
class CommentSectionsController:
    def __init__(self):
        self.comment_sections_orchestration: CommentSectionsOrchestration = di.create_comment_sections_orchestration()

    @route.get(
        "/posts/{post_public_id}/comments",
        auth=None,
        response={200: List[CommentResponseSchema], 404: NotOkResponseSchema}
    )
    def list_comments(self, post_public_id: UUID, cursor: Optional[str] = None, page_size: int = 20):
        """List top-level comments for a post (paginated)."""
        result = self.comment_sections_orchestration.list_comments(
            post_public_id=post_public_id, 
            cursor=cursor, 
            page_size=page_size
        )

        return Result.result_parser(
            result=result,
            ok_handler=lambda ok_value: (200, ok_value),
        )

    @route.post(
        "/posts/{post_public_id}/comments",
        auth=JWTAuth(),
        response={201: CommentResponseSchema, 401: NotOkResponseSchema, 404: NotOkResponseSchema},
    )
    def add_comment(self, request: HttpRequest, post_public_id: UUID, new_comment_data: NewCommentRequestSchema):
        """Add a new comment to a post."""
        user_id = request.user.id
        if not user_id:
            return 401, {"message": "unauthenticated", "static_msg": "UNAUTHORIZED"}

        result = self.comment_sections_orchestration.add_comment(
            post_public_id=post_public_id, 
            author_id=user_id, 
            content=new_comment_data.content, 
            parent_comment_id=new_comment_data.parent_public_id
        )

        return Result.result_parser(
            result=result,
            ok_handler=lambda ok_value: (201, ok_value),
        )
    
    @route.get(
        "/{comment_public_id}/thread",
        auth=None,
        response={200: CommentThreadResponseSchema, 404: NotOkResponseSchema}
    )
    def get_comment_thread(self, comment_public_id: UUID, cursor: Optional[str] = None, page_size: int = 10):
        """Retrieve a comment thread (root comment + paginated replies)."""
        result = self.comment_sections_orchestration.get_comment_thread(
            comment_public_id=comment_public_id, 
            cursor=cursor, 
            page_size=page_size
        )

        return Result.result_parser(
            result=result,
            ok_handler=lambda thread: (200, thread),
        )

    @route.put(
        "/{comment_public_id}",
        auth=JWTAuth(),
        response={200: CommentResponseSchema, 401: NotOkResponseSchema, 404: NotOkResponseSchema}
    )
    def update_comment(self, request: HttpRequest, comment_public_id: UUID, payload: UpdateCommentRequestSchema):
        """Update a comment (author only)."""
        actor_user_id = request.user.id
        if not actor_user_id:
            return 401, {"message": "unauthenticated", "static_msg": "UNAUTHORIZED"}

        result = self.comment_sections_orchestration.update_comment(
            comment_public_id=comment_public_id,
            actor_user_id=actor_user_id,
            new_text=payload.content,
        )

        return Result.result_parser(
            result=result,
            ok_handler=lambda comment: (200, comment),
        )

    @route.delete(
        "/{comment_public_id}",
        auth=JWTAuth(),
        response={204: None, 401: NotOkResponseSchema, 404: NotOkResponseSchema}
    )
    def delete_comment(self, request: HttpRequest, comment_public_id: UUID):
        """Soft-delete a comment (author only)."""
        actor_user_id = request.user.id
        if not actor_user_id:
            return 401, {"message": "unauthenticated", "static_msg": "UNAUTHORIZED"}

        result = self.comment_sections_orchestration.delete_comment(
            comment_public_id=comment_public_id,
            actor_user_id=actor_user_id,
        )

        return Result.result_parser(
            result=result,
            ok_handler=lambda _: (204, None),
        )

    @route.post(
        "/{comment_public_id}/vote",
        auth=JWTAuth(),
        response={
            200: NotOkResponseSchema, 
            400: NotOkResponseSchema, 
            401: NotOkResponseSchema, 
            404: NotOkResponseSchema, 
            500: ErrorResponseSchema
        },
    )
    def vote_on_comment(self, request: HttpRequest, comment_public_id: UUID, payload: VoteOnCommentRequestSchema):
        """Vote on a comment."""
        user_id = getattr(request.user, "id", None)
        if not user_id:
            return 401, {"message": "unauthenticated", "static_msg": "UNAUTHORIZED"}

        result = self.comment_sections_orchestration.vote_on_comment(
            comment_public_id=comment_public_id,
            voter_user_id=user_id,
            action=payload.action,
        )

        # return a dict with shape expected by NotOkResponseSchema on success
        return Result.result_parser(
            result=result,
            ok_handler=lambda value: (200, {"message": "ok", "static_msg": "comment.vote_success"})
        )
