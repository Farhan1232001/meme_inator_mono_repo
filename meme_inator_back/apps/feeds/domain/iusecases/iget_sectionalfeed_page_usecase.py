from abc import ABC, abstractmethod
from apps.feeds.domain.entities.sf_page_request_vo import SectionalFeedPageRequestVo
from apps.feeds.domain.entities.sf_page_response_vo import SectionalFeedPageResponseVo
from core.results import Result

class IGetSectionalfeedPageUsecase(ABC):
    """
    Usecase interface for retrieving a sectional feed page (duration-window cursor pagination).
    """

    @abstractmethod
    def execute(self, request_vo: SectionalFeedPageRequestVo) -> Result[SectionalFeedPageResponseVo]:
        """
        Execute the sectional-feed business logic.

        Steps (expected):
          - Use SectionalFeedsModel to compute duration windows and fetch posts per window
          - Build SectionalFeedResponseVo(duration_windows, next_cursor, has_more)
          - Return Result.ok(...) or Result.fail(...)
        """
        raise NotImplementedError
