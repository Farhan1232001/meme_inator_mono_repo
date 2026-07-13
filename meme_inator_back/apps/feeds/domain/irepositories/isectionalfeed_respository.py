# apps/feeds/domain/irepositories/isectionalfeed_repository.py
from abc import ABC, abstractmethod
from typing import Optional
from apps.feeds.domain.entities.sf_page_request_vo import SectionalFeedPageRequestVo
from apps.feeds.domain.entities.sf_page_response_vo import SectionalFeedPageResponseVo
from core.results import Result

class ISectionalfeedRepository(ABC):
    """
    Repository interface for sectional feeds.

    The repository should return Result[SectionalFeedResponseVo].
    """

    @abstractmethod
    def fetch_page(self, request_vo: SectionalFeedPageRequestVo) -> Result[SectionalFeedPageResponseVo]:
        """
        Fetch or compute the sectional feed response (windows + next_cursor + has_more).
        Implementation may delegate to SectionalFeedsModel or implement ORM queries directly.
        """
        raise NotImplementedError
