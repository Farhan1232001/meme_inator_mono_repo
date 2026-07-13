from abc import ABC, abstractmethod
from apps.feeds.domain.entities.gf_page_request_vo import GridfeedPageRequestVo
from apps.feeds.domain.entities.gf_page_response_vo import GridfeedPageResponseVo
from core.results import Result

class IGetGridfeedPageUsecase(ABC):
    """Interface for the GetGridfeedPage usecase."""

    @abstractmethod
    def execute(self, request_vo: GridfeedPageRequestVo) -> Result[GridfeedPageResponseVo]:
        """
        Execute the business logic to produce a grid feed page.

        Steps (expected in an implementation, matching your sequence diagram):
        - call repository.fetch_page(request_vo) -> (next_cursor, raw_posts)
        - call PostHydrator.hydrate(raw_posts) -> List[PostEntity]
        - build GfPageResponseVo(next_cursor, results)
        - wrap in a Result subtype
        """
        ...
