# apps/feeds/repositories/gridfeed_repository.py
from typing import Optional

from apps.feeds.domain.entities.gf_page_request_vo import GridfeedPageRequestVo
from apps.feeds.domain.entities.gf_page_response_vo import GridfeedPageResponseVo
from apps.feeds.domain.irepositories.igridfeed_repository import IGridfeedRepository
from apps.feeds.infrastructure.models.gridfeeds_model import GridfeedsModel
from core.results import Ok, Result


class GridfeedRepository(IGridfeedRepository):
    """
    Concrete repository for grid feeds.

    Responsibilities:
      - Adapt GridfeedPageRequestVo to GridfeedsModel
      - Return GridfeedPageResponseVo wrapped in Result
      - NO hydration
      - NO business rules
    """

    def __init__(self, gridfeeds_model: GridfeedsModel):
        self._model = gridfeeds_model

    def fetch_page(
        self,
        request_vo: GridfeedPageRequestVo
    ) -> Result[GridfeedPageResponseVo]:
        """
        Fetch a grid feed page.

        Flow:
          - delegate to GridfeedsModel.get_grid_feed(...)
          - adapt PageResult → GridfeedPageResponseVo
          - wrap in Result
        """
        page_response_vo: GridfeedPageResponseVo = self._model.get_grid_feed(
            feed_type=request_vo.feed_type,
            cursor=request_vo.cursor,
            page_size=request_vo.page_size,
            requesting_user_id=request_vo.requesting_user_id,
            filters=request_vo.filters, 
        )
        return Ok(page_response_vo)
