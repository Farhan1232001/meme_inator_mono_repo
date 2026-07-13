from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from datetime import datetime

from django.db.models import QuerySet


class IRankingStrategy(ABC):
    """
    Strategy interface for ranking posts within a time window.
    """

    @abstractmethod
    def apply(
        self,
        qs: QuerySet,
        start: datetime,
        end: datetime,
        requesting_user_id: Optional[UUID] = None,
    ) -> QuerySet:
        """
        Apply ordering / annotations to a PostModel queryset.

        Must:
          - NOT evaluate the queryset
          - ONLY apply annotations/orderings
        """
        raise NotImplementedError
