from datetime import datetime, timedelta
from typing import List, Optional, Union
from uuid import UUID

from django.utils import timezone as dj_timezone

from apps.feeds.domain.entities.duration_window_vo import DurationWindow
from apps.feeds.domain.entities.feed_filters_vo import FeedFilters
from apps.feeds.domain.entities.sf_page_response_vo import SectionalFeedPageResponseVo
from apps.feeds.domain.enums.feed_type import SectionalFeedType
from apps.feeds.infrastructure.rankings.ipopularity_strategy import IRankingStrategy
from apps.feeds.infrastructure.rankings.simple_popularity_strategy import SimplePopularityRanking
from apps.posts.domain.entities.post_entity import PostEntity
from apps.posts.infrastructure.models.post_model import PostModel


UTC = dj_timezone.get_fixed_timezone(0)


class SectionalFeedsModel:
    """
    Responsible for computing duration windows and fetching posts per window.
    Returns a SectionalFeedPageResponseVo directly.
    """

    def __init__(self, ranking_strategy: Optional[IRankingStrategy] = None):
        self._ranking_strategy = ranking_strategy or SimplePopularityRanking()

    def get_sectional_feed(
        self,
        feed_type: Union[SectionalFeedType, str],
        duration_unit: str,  # 'day' | 'week' | 'month'
        duration_window_size: int = 3,
        cursor: Optional[str] = None,
        requesting_user_id: Optional[UUID] = None,
        filters: Optional[FeedFilters] = None,
    ) -> SectionalFeedPageResponseVo:

        if isinstance(feed_type, str):
            try:
                feed_type = SectionalFeedType(feed_type)
            except ValueError:
                raise ValueError(f"Unsupported feed_type: {feed_type}")

        anchor_dt = self._decode_cursor_or_default(cursor)
        windows = self._compute_windows(anchor_dt, duration_unit, duration_window_size)

        for w in windows:
            w.posts = self._fetch_posts_for_window(
                w.window_start,
                w.window_end,
                feed_type,
                requesting_user_id,
                filters
            )

        next_cursor = self._compute_next_cursor_from_windows(windows)
        has_more = self._determine_has_more(windows)

        return SectionalFeedPageResponseVo(
            duration_windows=windows,
            next_cursor=next_cursor,
            has_more=has_more,
        )

    # ------------------------------------------------------------------
    # Cursor handling
    # ------------------------------------------------------------------
    def _decode_cursor_or_default(self, cursor: Optional[str]) -> datetime:
        """
        Decode cursor to a tz-aware UTC datetime.
        Cursor is expected to be ISO-8601, optionally ending with 'Z'.
        """
        if not cursor:
            return dj_timezone.now().astimezone(UTC)

        try:
            dt = datetime.fromisoformat(cursor.replace("Z", "+00:00"))
            if not dj_timezone.is_aware(dt):
                dt = dj_timezone.make_aware(dt, UTC)
            return dt.astimezone(UTC)
        except Exception:
            raise ValueError("Invalid cursor format; expected ISO-8601")

    # ------------------------------------------------------------------
    # Window computation
    # ------------------------------------------------------------------
    def _compute_windows(
        self,
        anchor: datetime,
        duration_unit: str,
        window_size: int,
    ) -> List[DurationWindow]:

        if not dj_timezone.is_aware(anchor):
            raise ValueError("anchor datetime must be timezone-aware")

        anchor = anchor.astimezone(UTC)
        windows: List[DurationWindow] = []

        for i in range(window_size):
            if duration_unit == "day":
                end = self._floor_day(anchor) - timedelta(days=i)
                start = end - timedelta(days=1)
                key = start.date().isoformat()

            elif duration_unit == "week":
                end = self._floor_week(anchor) - timedelta(weeks=i)
                start = end - timedelta(weeks=1)
                iso = start.isocalendar()
                key = f"{iso.year}-W{iso.week:02d}"

            elif duration_unit == "month":
                end = self._floor_month(anchor, offset_months=i)
                start = self._floor_month(anchor, offset_months=i + 1)
                key = f"{start.year}-{start.month:02d}"

            else:
                raise ValueError(f"Unsupported duration_unit: {duration_unit}")

            windows.append(
                DurationWindow(
                    window_start=start,
                    window_end=end,
                    posts=[],
                    window_key=key,
                )
            )

        return windows

    def _floor_day(self, dt: datetime) -> datetime:
        return dt.astimezone(UTC).replace(hour=0, minute=0, second=0, microsecond=0)

    def _floor_week(self, dt: datetime) -> datetime:
        dt_utc = dt.astimezone(UTC)
        start = dt_utc - timedelta(days=dt_utc.weekday())
        return self._floor_day(start)

    def _floor_month(self, dt: datetime, offset_months: int = 0) -> datetime:
        dt_utc = dt.astimezone(UTC)
        year = dt_utc.year
        month = dt_utc.month - offset_months

        while month <= 0:
            month += 12
            year -= 1

        return datetime(year, month, 1, tzinfo=UTC)

    # ------------------------------------------------------------------
    # Fetching & ranking
    # ------------------------------------------------------------------
    def _fetch_posts_for_window(
        self,
        start: datetime,
        end: datetime,
        feed_type: Union[SectionalFeedType, str],
        requesting_user_id: Optional[UUID],
        filters: Optional[FeedFilters], 
    ) -> List[PostEntity]:

        if not dj_timezone.is_aware(start) or not dj_timezone.is_aware(end):
            raise ValueError("start and end must be timezone-aware")

        qs = PostModel.objects.filter(
            created_on__gte=start,
            created_on__lt=end,
            is_deleted=False,
            is_flagged=False,
        )

        qs = self._apply_filters(qs, filters) 

        qs = self._ranking_strategy.apply(
            qs=qs,
            start=start,
            end=end,
            requesting_user_id=requesting_user_id,
        )[:50]

        return [
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
            for row in qs
        ]

    # TODO: gridfeeds_model.py has duplicate method. Pls follow DRY principle. 
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

    # ------------------------------------------------------------------
    # Pagination helpers
    # ------------------------------------------------------------------
    def _compute_next_cursor_from_windows(
        self,
        windows: List[DurationWindow],
    ) -> Optional[str]:

        if not windows:
            return None

        return (
            windows[-1]
            .window_start
            .astimezone(UTC)
            .isoformat()
            .replace("+00:00", "Z")
        )

    def _determine_has_more(self, windows: List[DurationWindow]) -> bool:
        return bool(windows and windows[-1].posts)
