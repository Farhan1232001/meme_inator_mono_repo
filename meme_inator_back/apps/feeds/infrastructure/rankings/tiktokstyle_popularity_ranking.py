from typing import Optional
from uuid import UUID
from datetime import datetime

from django.db.models import QuerySet

from apps.feeds.popularity.base import PopularityStrategy


class TikTokStylePopularityRanking(PopularityStrategy):
    """
    Placeholder for advanced ranking:
      - time decay
      - engagement velocity
      - user affinity
      - exploration vs exploitation
    """

    def apply(
        self,
        qs: QuerySet,
        start: datetime,
        end: datetime,
        requesting_user_id: Optional[UUID] = None,
    ) -> QuerySet:
        raise NotImplementedError(
            "TikTok-style popularity ranking is not implemented yet"
        )
