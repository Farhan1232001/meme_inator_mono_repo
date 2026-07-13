# apps/feeds/repositories/sectionalfeed_repository.py
from typing import Optional
from apps.feeds.domain.irepositories.isectionalfeed_respository import ISectionalfeedRepository
from apps.feeds.domain.entities.sf_page_request_vo import SectionalFeedPageRequestVo
from apps.feeds.domain.entities.sf_page_response_vo import SectionalFeedPageResponseVo
from apps.feeds.infrastructure.models.sectionalfeeds_model import SectionalFeedsModel
from core.results import Result, Ok, Error

class SectionalfeedRepository(ISectionalfeedRepository):
    """
    Concrete repository delegating to SectionalFeedsModel and returning Result[SectionalFeedResponseVo].
    """

    def __init__(self, sectionalfeed_model: SectionalFeedsModel):
        self._model = sectionalfeed_model

    def fetch_page(self, request_vo: SectionalFeedPageRequestVo) -> Result[SectionalFeedPageResponseVo]:
        page_response_vo: SectionalFeedPageResponseVo = self._model.get_sectional_feed(
            feed_type=request_vo.feed_type,
            duration_unit=request_vo.duration_unit,
            duration_window_size=request_vo.duration_window_size,
            cursor=request_vo.cursor,
            requesting_user_id=None,
            filters=request_vo.filters, 
        )

        return Ok(page_response_vo)