from enum import Enum
from typing import Any, Dict, Optional, Union

from apps.feeds.domain.enums.feed_type import FeedType, GridFeedType, SectionalFeedType

# TODO
# ******** CHATGPT GENERATED: Output has NOT been checked *************
# Validate configuration shape/structure before using it everywhere. 

# ---------------------------------------------------------------------
# Shared conventions
# ---------------------------------------------------------------------
# visibility:
#   - public  => no login required, generally safe to expose broadly
#   - private => requires an authenticated requester or a user-specific context
#
# auth_required:
#   - whether the endpoint/feed should reject anonymous access
#
# requires_requesting_user_id:
#   - whether the backend logic needs the requesting user's ID
#
# requires_author_username:
#   - whether the feed can/should be narrowed by author username
#
# supports_*:
#   - whether a filter is meaningful for that feed type
#
# cache_scope:
#   - "global" => same response for everyone
#   - "user"   => response varies by requesting_user_id
#   - "author" => response varies by author_username
#   - "none"   => do not cache
#
# ranking_strategy:
#   - a string label you can map to a strategy class in your DI/config layer
# ---------------------------------------------------------------------


# FEED_CONFIG is a dict consisting of dicts.
# 1st level: general FeedTypes
# 2nd level: Particular FeedTypes such as GridFeedType and SectionalFeedType
FEED_CONFIG: Dict[FeedType, Dict[Any, Dict[str, Any]]] = {
    FeedType.GRID: {
        GridFeedType.RECENT: {
            "feed_type": FeedType.GRID,
            "visibility": "public",
            "auth_required": False,
            "requires_requesting_user_id": False,
            "requires_author_username": False,

            "supports_cursor": True,
            "pagination_mode": "cursor",
            "default_page_size": 10,
            "max_page_size": 1000,

            "default_ordering": ["-created_on", "-post_id"],
            "ranking_strategy": None,

            "hydrate_urls": True,
            "hide_deleted": True,
            "hide_flagged": True,

            "supports_filters": {
                "author_id": True,
                "author_username": True,
                "hashtag": True,
                "language": True,
                "content_type": True,
                "min_likes": True,
            },

            "cache_scope": "global",
            "cache_ttl_seconds": 60,
        },

        GridFeedType.RANDOMIZED: {
            "feed_type": FeedType.GRID,
            "visibility": "public",
            "auth_required": False,
            "requires_requesting_user_id": False,
            "requires_author_username": False,

            "supports_cursor": True,
            "pagination_mode": "cursor",
            "default_page_size": 10,
            "max_page_size": 1000,

            "default_ordering": None,
            "ranking_strategy": "randomized",

            "hydrate_urls": True,
            "hide_deleted": True,
            "hide_flagged": True,

            "supports_filters": {
                "author_id": True,
                "author_username": True,
                "hashtag": True,
                "language": True,
                "content_type": True,
                "min_likes": True,
            },

            "cache_scope": "none",
            "cache_ttl_seconds": 0,
        },

        GridFeedType.VIDEOS_ONLY: {
            "feed_type": FeedType.GRID,
            "visibility": "public",
            "auth_required": False,
            "requires_requesting_user_id": False,
            "requires_author_username": False,

            "supports_cursor": True,
            "pagination_mode": "cursor",
            "default_page_size": 10,
            "max_page_size": 1000,

            "default_ordering": ["-created_on", "-post_id"],
            "ranking_strategy": None,
            "media_filter": "video",

            "hydrate_urls": True,
            "hide_deleted": True,
            "hide_flagged": True,

            "supports_filters": {
                "author_id": True,
                "author_username": True,
                "hashtag": True,
                "language": True,
                "content_type": False,
                "min_likes": True,
            },

            "cache_scope": "global",
            "cache_ttl_seconds": 120,
        },

        GridFeedType.IMAGES_ONLY: {
            "feed_type": FeedType.GRID,
            "visibility": "public",
            "auth_required": False,
            "requires_requesting_user_id": False,
            "requires_author_username": False,

            "supports_cursor": True,
            "pagination_mode": "cursor",
            "default_page_size": 10,
            "max_page_size": 1000,

            "default_ordering": ["-created_on", "-post_id"],
            "ranking_strategy": None,
            "media_filter": "image",

            "hydrate_urls": True,
            "hide_deleted": True,
            "hide_flagged": True,

            "supports_filters": {
                "author_id": True,
                "author_username": True,
                "hashtag": True,
                "language": True,
                "content_type": False,
                "min_likes": True,
            },

            "cache_scope": "global",
            "cache_ttl_seconds": 120,
        },

        GridFeedType.MOST_COMMENTED: {
            "feed_type": FeedType.GRID,
            "visibility": "public",
            "auth_required": False,
            "requires_requesting_user_id": False,
            "requires_author_username": False,

            "supports_cursor": True,
            "pagination_mode": "cursor",
            "default_page_size": 10,
            "max_page_size": 1000,

            "default_ordering": ["-comments_count", "-created_on", "-post_id"],
            "ranking_strategy": "most_commented",

            "hydrate_urls": True,
            "hide_deleted": True,
            "hide_flagged": True,

            "supports_filters": {
                "author_id": True,
                "author_username": True,
                "hashtag": True,
                "language": True,
                "content_type": True,
                "min_likes": True,
            },

            "cache_scope": "global",
            "cache_ttl_seconds": 60,
        },

        GridFeedType.USER_PROFILE: {
            "feed_type": FeedType.GRID,
            "visibility": "private",
            "auth_required": True,
            "requires_requesting_user_id": True,
            "requires_author_username": True,

            "supports_cursor": True,
            "pagination_mode": "cursor",
            "default_page_size": 10,
            "max_page_size": 1000,

            "default_ordering": ["-created_on", "-post_id"],
            "ranking_strategy": None,

            "hydrate_urls": True,
            "hide_deleted": True,
            "hide_flagged": True,

            "supports_filters": {
                "author_id": False,
                "author_username": True,
                "hashtag": True,
                "language": True,
                "content_type": True,
                "min_likes": True,
            },

            "cache_scope": "author",
            "cache_ttl_seconds": 30,
        },

        GridFeedType.FRIENDS_POSTS: {
            "feed_type": FeedType.GRID,
            "visibility": "private",
            "auth_required": True,
            "requires_requesting_user_id": True,
            "requires_author_username": False,

            "supports_cursor": True,
            "pagination_mode": "cursor",
            "default_page_size": 10,
            "max_page_size": 1000,

            "default_ordering": ["-created_on", "-post_id"],
            "ranking_strategy": "friends_only",

            "hydrate_urls": True,
            "hide_deleted": True,
            "hide_flagged": True,

            "supports_filters": {
                "author_id": True,
                "author_username": True,
                "hashtag": True,
                "language": True,
                "content_type": True,
                "min_likes": True,
            },

            "cache_scope": "user",
            "cache_ttl_seconds": 30,
        },

        GridFeedType.FOLLOWINGS_POSTS: {
            "feed_type": FeedType.GRID,
            "visibility": "private",
            "auth_required": True,
            "requires_requesting_user_id": True,
            "requires_author_username": False,

            "supports_cursor": True,
            "pagination_mode": "cursor",
            "default_page_size": 10,
            "max_page_size": 1000,

            "default_ordering": ["-created_on", "-post_id"],
            "ranking_strategy": "following_only",

            "hydrate_urls": True,
            "hide_deleted": True,
            "hide_flagged": True,

            "supports_filters": {
                "author_id": True,
                "author_username": True,
                "hashtag": True,
                "language": True,
                "content_type": True,
                "min_likes": True,
            },

            "cache_scope": "user",
            "cache_ttl_seconds": 30,
        },

        GridFeedType.USER_UPVOTED_POSTS: {
            "feed_type": FeedType.GRID,
            "visibility": "private",
            "auth_required": True,
            "requires_requesting_user_id": True,
            "requires_author_username": False,
            "supports_cursor": True,
            "pagination_mode": "cursor",
            "default_page_size": 10,
            "max_page_size": 1000,
            "default_ordering": ["-created_on", "-post_id"],
            "ranking_strategy": None,
            "hydrate_urls": True,
            "hide_deleted": True,
            "hide_flagged": True,
            "supports_filters": {
                "author_id": True,
                "author_username": True,
                "hashtag": True,
                "language": True,
                "content_type": True,
                "min_likes": True,
            },
            "cache_scope": "user",
            "cache_ttl_seconds": 60,
        },
        GridFeedType.COMMENTED_FEEDS: {
            "feed_type": FeedType.GRID,
            "visibility": "private",
            "auth_required": True,
            "requires_requesting_user_id": True,
            "requires_author_username": False,
            "supports_cursor": True,
            "pagination_mode": "cursor",
            "default_page_size": 10,
            "max_page_size": 1000,
            "default_ordering": ["-created_on", "-post_id"],
            "ranking_strategy": None,
            "hydrate_urls": True,
            "hide_deleted": True,
            "hide_flagged": True,
            "supports_filters": {
                "author_id": True,
                "author_username": True,
                "hashtag": True,
                "language": True,
                "content_type": True,
                "min_likes": True,
            },
            "cache_scope": "user",
            "cache_ttl_seconds": 60,
        },
    },

    FeedType.SECTIONAL: {
        SectionalFeedType.POPULAR_TODAY: {
            "feed_type": FeedType.SECTIONAL,
            "visibility": "public",
            "auth_required": False,
            "requires_requesting_user_id": False,
            "requires_author_username": False,

            "supports_cursor": True,
            "pagination_mode": "windowed_cursor",
            "default_page_size": 10,
            "max_page_size": 1000,

            "allowed_duration_units": ["day"],
            "default_duration_unit": "day",
            "default_duration_window_size": 3,
            "max_duration_window_size": 50,

            "ranking_strategy": "simple_popularity",

            "hydrate_urls": True,
            "hide_deleted": True,
            "hide_flagged": True,

            "supports_filters": {
                "author_id": True,
                "author_username": True,
                "hashtag": True,
                "language": True,
                "content_type": True,
                "min_likes": True,
            },

            "cache_scope": "global",
            "cache_ttl_seconds": 300,
        },

        SectionalFeedType.POPULAR_WEEKLY: {
            "feed_type": FeedType.SECTIONAL,
            "visibility": "public",
            "auth_required": False,
            "requires_requesting_user_id": False,
            "requires_author_username": False,

            "supports_cursor": True,
            "pagination_mode": "windowed_cursor",
            "default_page_size": 10,
            "max_page_size": 1000,

            "allowed_duration_units": ["week"],
            "default_duration_unit": "week",
            "default_duration_window_size": 3,
            "max_duration_window_size": 50,

            "ranking_strategy": "simple_popularity",

            "hydrate_urls": True,
            "hide_deleted": True,
            "hide_flagged": True,

            "supports_filters": {
                "author_id": True,
                "author_username": True,
                "hashtag": True,
                "language": True,
                "content_type": True,
                "min_likes": True,
            },

            "cache_scope": "global",
            "cache_ttl_seconds": 900,
        },

        SectionalFeedType.POPULAR_MONTHLY: {
            "feed_type": FeedType.SECTIONAL,
            "visibility": "public",
            "auth_required": False,
            "requires_requesting_user_id": False,
            "requires_author_username": False,

            "supports_cursor": True,
            "pagination_mode": "windowed_cursor",
            "default_page_size": 10,
            "max_page_size": 1000,

            "allowed_duration_units": ["month"],
            "default_duration_unit": "month",
            "default_duration_window_size": 3,
            "max_duration_window_size": 50,

            "ranking_strategy": "simple_popularity",

            "hydrate_urls": True,
            "hide_deleted": True,
            "hide_flagged": True,

            "supports_filters": {
                "author_id": True,
                "author_username": True,
                "hashtag": True,
                "language": True,
                "content_type": True,
                "min_likes": True,
            },

            "cache_scope": "global",
            "cache_ttl_seconds": 1800,
        },

        SectionalFeedType.USER_PROFILE: {
            "feed_type": FeedType.SECTIONAL,
            "visibility": "private",
            "auth_required": True,
            "requires_requesting_user_id": True,
            "requires_author_username": True,

            "supports_cursor": True,
            "pagination_mode": "windowed_cursor",
            "default_page_size": 10,
            "max_page_size": 1000,

            "allowed_duration_units": ["day", "week", "month"],
            "default_duration_unit": "day",
            "default_duration_window_size": 3,
            "max_duration_window_size": 50,

            "ranking_strategy": "profile_activity",

            "hydrate_urls": True,
            "hide_deleted": True,
            "hide_flagged": True,

            "supports_filters": {
                "author_id": False,
                "author_username": True,
                "hashtag": True,
                "language": True,
                "content_type": True,
                "min_likes": True,
            },

            "cache_scope": "author",
            "cache_ttl_seconds": 60,
        },
    },
}


def get_feed_config(feed_type: Union[GridFeedType, SectionalFeedType]) -> Dict[str, Any]:
    # Determine which top-level feed type this belongs to
    if feed_type in FEED_CONFIG[FeedType.GRID]:
        return FEED_CONFIG[FeedType.GRID][feed_type]

    if feed_type in FEED_CONFIG[FeedType.SECTIONAL]:
        return FEED_CONFIG[FeedType.SECTIONAL][feed_type]

    raise ValueError(f"Unsupported feed_type: {feed_type}")


def is_private_feed(feed_type: Union[GridFeedType, SectionalFeedType]) -> bool:
    return get_feed_config(feed_type)["visibility"] == "private"