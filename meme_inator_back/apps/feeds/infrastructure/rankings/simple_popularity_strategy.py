from typing import Optional
from uuid import UUID
from datetime import datetime

from django.db.models import F, QuerySet

from apps.feeds.infrastructure.rankings.ipopularity_strategy import IRankingStrategy



class SimplePopularityRanking(IRankingStrategy):
    """
    Simple ranking:
      score = likes + comments
    """

    def apply(
        self,
        qs: QuerySet,
        start: datetime,
        end: datetime,
        requesting_user_id: Optional[UUID] = None,
    ) -> QuerySet:

        return (
            qs.annotate(
                score=F("upvotes_count") + F("comments_count")
            )
            .order_by("-score", "-created_on")
        )
