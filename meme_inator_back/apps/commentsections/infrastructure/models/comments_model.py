import uuid
from django.db import models, transaction
from django.conf import settings
from django.db.models import F
from django.db.models import Q
from django.utils.dateparse import parse_datetime
from typing import Optional, Tuple, List


class CommentModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    public_id = models.UUIDField(default=uuid.uuid7, editable=False, unique=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    post = models.ForeignKey(
        "posts.PostModel",
        on_delete=models.CASCADE,
        related_name="comments"
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies"
    )

    content = models.TextField()
    level = models.PositiveSmallIntegerField(default=0)

    reply_count = models.PositiveIntegerField(default=0)
    upvote_count = models.PositiveIntegerField(default=0)
    downvote_count = models.PositiveIntegerField(default=0)

    is_deleted = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "commentsections"
        db_table = "commentsections_commentmodel"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["post", "parent", "created_at"]),
            models.Index(fields=["public_id"]),
        ]

    # ------------------------------------------------------------------
    # Factory
    # ------------------------------------------------------------------

    @classmethod
    def create_new(
        self,
        *,
        post,
        author,
        text: str,
        parent: "CommentModel | None" = None,
    ) -> "CommentModel":
        """
        Factory used by repository.
        Handles level calculation + reply count updates.
        """
        with transaction.atomic():
            level = parent.level + 1 if parent else 0

            comment = self.objects.create(
                post=post,
                author=author,
                parent=parent,
                content=text,
                level=level,
            )

            if parent:
                self.objects.filter(id=parent.id).update(
                    reply_count=F("reply_count") + 1
                )

            return comment

    # ------------------------------------------------------------------
    # ORM-facing helpers (moved queries here)
    # ------------------------------------------------------------------

    @classmethod
    def fetch_by_public_id(self, public_id: uuid.UUID) -> Optional[CommentModel]:
        """
        Returns a CommentModel instance or None. Includes related objects for repo mapping.
        """
        # select_related = “When you fetch comments, also fetch these FK-related objects in the same SQL query”
        return self.objects.select_related("author", "post", "parent").filter(public_id=public_id).first()

    @classmethod
    def fetch_parent_by_public_id(self, parent_public_id: uuid.UUID) -> Optional["CommentModel"]:
        """
        Return parent model instance or None.
        """
        if not parent_public_id:
            return None
        return self.objects.filter(public_id=parent_public_id).first()

    @classmethod
    def list_with_pagination(
        self,
        base_query: Q,
        cursor: Optional[str],
        page_size: int
    ) -> Tuple[List["CommentModel"], Optional[str]]:
        """
        Return (items, next_cursor) where items is a list of CommentModel instances.
        This encapsulates pagination and ORM details.
        """
        qs = self.objects.select_related("author", "post").filter(base_query, is_deleted=False).order_by("-created_at")
        if cursor and (dt := parse_datetime(cursor)):
            qs = qs.filter(created_at__lt=dt)

        items = list(qs[:page_size + 1])
        has_more = len(items) > page_size
        results = items[:page_size] if has_more else items

        next_cursor = results[-1].created_at.isoformat() if has_more and results else None
        return results, next_cursor

    # ------------------------------------------------------------------
    # Mutations (called by repository)
    # ------------------------------------------------------------------

    def update_text(self, new_text: str) -> None:
        self.content = new_text
        self.save(update_fields=["content", "updated_at"])

    def soft_delete(self) -> None:
        if self.is_deleted:
            return

        with transaction.atomic():
            self.is_deleted = True
            self.save(update_fields=["is_deleted", "updated_at"])

            if self.parent_id:
                CommentModel.objects.filter(id=self.parent_id).update(
                    reply_count=F("reply_count") - 1
                )

    def get_vote_stats(self) -> dict:
        """Get current vote statistics."""
        return {
            'likes': self.upvote_count,
            'dislikes': self.downvote_count,
        }
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        return f"Comment({self.public_id})"
