from enum import Enum
from typing import Dict

class FeedType(str, Enum):
    SECTIONAL = 'sectional'
    GRID = 'grid'

    
class GridFeedType(str, Enum):
    RECENT = "recent"
    RANDOMIZED = "randomized"
    VIDEOS_ONLY = "videos_only"
    IMAGES_ONLY = "images_only"
    MOST_COMMENTED = "most_commented"
    USER_PROFILE = "user_profile"
    FRIENDS_POSTS = "friends_posts"
    FOLLOWINGS_POSTS = "followings_posts"
    USER_UPVOTED_POSTS = "user_upvoted_posts"
    COMMENTED_FEEDS = "commented_feeds"

    @staticmethod
    def get_gridfeed_values() -> list[str]:
        return [item.value for item in GridFeedType]


class SectionalFeedType(str, Enum):
    POPULAR_TODAY = "popular-today"
    POPULAR_WEEKLY = "popular-weekly"
    POPULAR_MONTHLY = "popular-monthly"
    USER_PROFILE = "user_profile"


    @staticmethod
    def get_sectionalfeed_values() -> list[str]:
        return [item.value for item in SectionalFeedType]