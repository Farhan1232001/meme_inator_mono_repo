
from dataclasses import dataclass

from apps.feeds.domain.enums.feed_type import FeedType


@dataclass
class FeedPreferencesEntity:
    default_feed_type: str # GridFeedType or SectionalFeedType however, not USER_PROFILE feed
    feed_grid_column_number: int
    scroll_speed: float

    def set_default_feed_type(self, feed_type: FeedType) -> None:
        self.default_feed_type = feed_type

    def set_feed_grid_column_number(self, num: int = 3):
        self.feed_grid_column_number = num

    def set_scroll_speed(self, speedFloat: float):
        self.scroll_speed = speedFloat