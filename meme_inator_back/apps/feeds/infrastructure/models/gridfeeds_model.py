# apps/feeds/infrastructure/models/gridfeeds_model.py

from datetime import datetime, timezone as dt_timezone
from typing import Optional, Tuple, Union, Callable, Dict
from uuid import UUID
import base64

from django.db.models import QuerySet, Q
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from apps.feeds.domain.entities.feed_filters_vo import FeedFilters
from apps.feeds.domain.entities.gf_page_response_vo import GridfeedPageResponseVo
from apps.feeds.domain.enums.feed_type import GridFeedType
from apps.posts.domain.entities.post_entity import PostEntity
from apps.posts.infrastructure.models.post_model import PostModel
from apps.posts.infrastructure.models.post_vote_model import PostVoteModel
from apps.users.infrastructure.models.fellowship_model import FellowshipModel
from apps.users.infrastructure.models.friendship_model import FriendshipModel
from core.results import NotOk


class GridfeedsModel:
    """
    High-level model/service that builds and paginates the various grid feed querysets.

    Rules:
      - All datetime creation / normalization uses django.utils.timezone
      - All datetimes are timezone-aware (UTC)
      - Cursor pagination uses (created_on DESC, post_id DESC)
    """

    # Build the dispatch table for feed handlers
    def __init__(self):
        # TODO: Is this efficient? creating dictionary every time instace is created?
        self._feed_query_handlers: Dict[GridFeedType, Callable[[Optional[UUID], Optional[FeedFilters]], QuerySet]] = {
            GridFeedType.RECENT: 
                lambda requesting_user_id, filters: 
                    self._recent_queryset(),
            GridFeedType.RANDOMIZED: 
                lambda requesting_user_id, filters: 
                    self._randomized_queryset(),
            GridFeedType.VIDEOS_ONLY: 
                lambda requesting_user_id, filters: 
                    self._media_type_queryset("video"),
            GridFeedType.IMAGES_ONLY: 
                lambda requesting_user_id, filters: 
                    self._media_type_queryset("image"),
            GridFeedType.MOST_COMMENTED: 
                lambda requesting_user_id, filters: 
                    self._most_commented_queryset(),
            GridFeedType.USER_PROFILE: 
                lambda requesting_user_id, filters: 
                    self._user_profile_queryset(requesting_user_id, filters),
            GridFeedType.FRIENDS_POSTS: 
                lambda requesting_user_id, filters: 
                    self._friends_posts_queryset(requesting_user_id),
            GridFeedType.FOLLOWINGS_POSTS: 
                lambda requesting_user_id, filters: 
                    self._following_posts_queryset(requesting_user_id),
            GridFeedType.USER_UPVOTED_POSTS: 
                lambda requesting_user_id, filters: 
                    self._user_upvoted_memes_queryset(requesting_user_id),
            GridFeedType.COMMENTED_FEEDS: 
                lambda requesting_user_id, filters: 
                    self._commented_feeds_queryset(requesting_user_id),
        }

    # -----------------------
    # Public (single entry)
    # -----------------------
    def get_grid_feed(
        self,
        feed_type: Union[GridFeedType, str],
        cursor: Optional[str],
        page_size: int = 10,
        requesting_user_id: Optional[UUID] = None,
        filters: Optional[FeedFilters] = None,
    ) -> GridfeedPageResponseVo:
        if isinstance(feed_type, str):
            try:
                feed_type = GridFeedType(feed_type)
            except ValueError:
                raise ValueError(f"unsupported feed_type: {feed_type}")

        # Get the appropriate handler for this feed type. feed_type maps to corresponding feed query method. Better approach then using if-else chains. 
        feed_query_handler = self._feed_query_handlers.get(feed_type)
        if feed_query_handler is None: raise ValueError(f"unsupported feed_type: {feed_type}")

        # For some feed types, we need to validate required parameters before calling handler
        if feed_type in (GridFeedType.FRIENDS_POSTS, GridFeedType.FOLLOWINGS_POSTS,
                         GridFeedType.USER_UPVOTED_POSTS,
                         GridFeedType.COMMENTED_FEEDS):
            if requesting_user_id is None:
                raise ValueError(f"requesting_user_id is required for feed_type '{feed_type.value}'")

        # Call the handler to get the base queryset
        qs = feed_query_handler(requesting_user_id, filters)

        # Apply common filters and then optional user filters
        qs = self._apply_common_filters(qs)
        qs = self._apply_filters(qs, filters)

        return self.paginate_cursor_queryset(qs, cursor=cursor, page_size=page_size)

    # -----------------------
    # Queryset builders
    # -----------------------
    def _base_queryset(self) -> QuerySet:
        return PostModel.objects.all()

    def _apply_common_filters(self, qs: QuerySet) -> QuerySet:
        return qs.filter(is_deleted=False, is_flagged=False)

    def _apply_filters(self, qs: QuerySet, filters: Optional[FeedFilters]) -> QuerySet:
        if not filters:
            return qs
        if filters.author_id:
            qs = qs.filter(author_id=filters.author_id)
        if filters.author_username:
            qs = qs.filter(author__user_name=filters.author_username)
        if filters.hashtag:
            qs = qs.filter(tags__contains=[filters.hashtag])  # adjust as per your tag field
        if filters.language:
            qs = qs.filter(language=filters.language)
        if filters.content_type:
            qs = qs.filter(post_type=filters.content_type)
        if filters.min_upvotes is not None:
            qs = qs.filter(upvotes_count__gte=filters.min_upvotes)
        return qs

    def _recent_queryset(self) -> QuerySet:
        return self._base_queryset().order_by("-created_on", "-post_id")

    # TODO: Not production ready: cursor pagination expects a deterministic order, this approach may break pagination. Better approach is to use a seeded random ordering. 
    def _randomized_queryset(self) -> QuerySet:
        return self._base_queryset().order_by('?')

    def _media_type_queryset(self, media_type: str) -> QuerySet:
        return (
            self._base_queryset()
            .filter(post_type__iexact=media_type)
            .order_by("-created_on", "-post_id")
        )

    def _most_commented_queryset(self) -> QuerySet:
        return (
            self._base_queryset()
            .order_by("-comments_count", "-created_on", "-post_id")
        )

    def _user_profile_queryset(self, requesting_user_id: Optional[UUID], filters: Optional[FeedFilters]) -> QuerySet:
        """
        Handler for USER_PROFILE feed type. It uses either the requesting_user_id or
        author_username from filters to determine which user's posts to return.
        """
        if filters and filters.author_username:
            from apps.users.infrastructure.models.user_model import UserModel
            try:
                user = UserModel.objects.only('id').get(user_name=filters.author_username)
                return self._user_posts_queryset(user.id)
            except UserModel.DoesNotExist:
                raise ValueError(f"User '{filters.author_username}' not found")
        elif requesting_user_id:
            return self._user_posts_queryset(requesting_user_id)
        else:
            raise ValueError("Either requesting_user_id or author_username filter is required for USER_PROFILE feed")

    def _user_posts_queryset(self, user_id: UUID) -> QuerySet:
        return (
            self._base_queryset()
            .filter(author_id=user_id)
            .order_by("-created_on", "-post_id")
        )

    def _friends_posts_queryset(self, requesting_user_id: UUID) -> QuerySet:
        # Get all active friendships where requesting_user_id is involved
        friendships = FriendshipModel.objects.filter(
            (Q(user_id=requesting_user_id) | Q(friend_id=requesting_user_id)),
            is_soft_deleted=False
        ).values_list('user_id', 'friend_id')

        # Build a set of distinct friend IDs (excluding self)
        friend_ids = set()
        for user_id, friend_id in friendships:
            if user_id == requesting_user_id:
                friend_ids.add(friend_id)
            else:
                friend_ids.add(user_id)

        # If no friends, return empty queryset
        if not friend_ids:
            return self._base_queryset().none()

        return self._base_queryset().filter(author_id__in=friend_ids).order_by("-created_on", "-post_id")

    def _following_posts_queryset(self, requesting_user_id: UUID) -> QuerySet:
        followed_user_ids = FellowshipModel.objects.filter(
            user_id=requesting_user_id,
            is_soft_deleted=False
        ).values_list('followed_user_id', flat=True)

        if not followed_user_ids:
            return self._base_queryset().none()

        return self._base_queryset().filter(author_id__in=followed_user_ids).order_by("-created_on", "-post_id")

    def _user_upvoted_memes_queryset(self, requesting_user_id: UUID) -> QuerySet:
        """Posts upvoted by the current user."""
        return self._base_queryset().filter(
            votes__user_id=requesting_user_id,
            votes__vote_type=PostVoteModel.VoteType.UPVOTE
        ).distinct().order_by("-created_on", "-post_id")

    def _commented_feeds_queryset(self, requesting_user_id: UUID) -> QuerySet:
        """Posts the current user has commented on."""
        return self._base_queryset().filter(
            comments__author_id=requesting_user_id
        ).distinct().order_by("-created_on", "-post_id")

    # -----------------------
    # Cursor pagination
    # -----------------------
    def paginate_cursor_queryset(
        self,
        qs: QuerySet,
        cursor: Optional[str],
        page_size: int = 10,
    ) -> GridfeedPageResponseVo:
        """
        Cursor pagination using (created_on DESC, post_id DESC) as the ordering/tiebreaker.
        """
        qs = qs.order_by("-created_on", "-post_id")

        if cursor:
            cursor_created_on, cursor_post_id = self.decode_cursor(cursor)
            qs = qs.filter(
                Q(created_on__lt=cursor_created_on)
                | Q(created_on=cursor_created_on, post_id__lt=cursor_post_id)
            )

        rows = list(qs[: page_size + 1])

        has_next = len(rows) > page_size
        results = rows[:page_size]

        next_cursor = None
        if has_next and results:
            last = results[-1]
            next_cursor = self.encode_cursor(
                created_on=self._ensure_aware_utc(last.created_on),
                post_id=last.post_id,
            )

        return GridfeedPageResponseVo(
            next_cursor=next_cursor,
            results=[
                PostEntity(
                    post_id=row.post_id,
                    imageURL=row.image_url,
                    thumbnailURL=row.thumbnail_url,
                    caption=row.caption,
                    createdOn=row.created_on,
                    post_type=row.post_type,
                    fileFormat=row.file_format,
                    upvotesCount=row.upvotes_count,
                    commentsCount=row.comments_count,
                    sharesCount=row.shares_count,
                    tags=row.tags or [],
                    isFlagged=row.is_flagged,
                    isDeleted=row.is_deleted,
                    visibility=row.visibility,
                    author=row.author_id,
                )
                for row in rows[:page_size]
            ]
        )

    # -----------------------
    # Cursor encode / decode
    # -----------------------
    def encode_cursor(self, created_on: datetime, post_id: UUID) -> str:
        created_on_utc = self._ensure_aware_utc(created_on)
        raw = f"{created_on_utc.isoformat()}|{post_id}"
        return base64.b64encode(raw.encode("utf-8")).decode("utf-8")

    def decode_cursor(self, cursor: str) -> Tuple[datetime, UUID]:
        try:
            decoded = base64.b64decode(cursor).decode("utf-8")
            ts_str, post_id_str = decoded.split("|", 1)
            parsed = datetime.fromisoformat(ts_str)
            created_on_utc = self._ensure_aware_utc(parsed)
            return created_on_utc, UUID(post_id_str)
        except Exception:
            raise ValueError("Invalid cursor")

    # -----------------------
    # Utilities
    # -----------------------
    def _ensure_aware_utc(self, dt: datetime) -> datetime:
        if timezone.is_aware(dt):
            return dt.astimezone(dt_timezone.utc)
        else:
            return dt.replace(tzinfo=dt_timezone.utc)

    def count_for_queryset(self, qs: QuerySet) -> int:
        return qs.count()