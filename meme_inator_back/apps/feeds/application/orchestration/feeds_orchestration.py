# apps/feeds/orchestration.py
from typing import Optional
from apps.feeds.domain.entities.gf_page_request_vo import GridfeedPageRequestVo
from apps.feeds.domain.entities.gf_page_response_vo import GridfeedPageResponseVo
from apps.feeds.domain.entities.sf_page_request_vo import SectionalFeedPageRequestVo
from apps.feeds.domain.entities.sf_page_response_vo import SectionalFeedPageResponseVo
from apps.feeds.domain.iusecases.iget_sectionalfeed_page_usecase import IGetSectionalfeedPageUsecase
from core.results import Result
from apps.feeds.domain.iusecases.iget_gridfeed_page_usecase import IGetGridfeedPageUsecase

class FeedsOrchestration:
    """
    Orchestration layer: adapts controller-level inputs to usecases and adapts usecase results to controller-friendly responses.
    This layer coordinates multiple usecases when necessary and handles high-level concerns (auth propagation, metrics, logs).
    """

    def __init__(
            self, 
            get_gridfeed_usecase: IGetGridfeedPageUsecase,
            get_sectional_feed_usecase: IGetSectionalfeedPageUsecase
        ):
        self._get_gridfeed_usecase = get_gridfeed_usecase
        self._get_sectionalfeed_usecase = get_sectional_feed_usecase

    def get_gridfeed_page(self, request_vo: GridfeedPageRequestVo) -> Result[GridfeedPageResponseVo]:
        """
        """
        return self._get_gridfeed_usecase.execute(
            request_vo=request_vo
        )


    def get_sectional_feed_page(self, request_vo: SectionalFeedPageRequestVo) -> Result[SectionalFeedPageResponseVo]:
        """
        """
        return self._get_sectionalfeed_usecase.execute(
            request_vo=request_vo
        )
