from apps.feeds.application.dtos.duration_window_schema import DurationWindowSchema
from apps.feeds.application.dtos.sf_page_response_schema import SfPageResponseSchema
from apps.feeds.domain.entities.duration_window_vo import DurationWindow
from apps.feeds.domain.entities.sf_page_response_vo import SectionalFeedPageResponseVo


def map_duration_window_vo_to_schema(vo: DurationWindow) -> DurationWindowSchema:
    """
    Map a domain DurationWindow VO to its API schema representation.
    """
    return DurationWindowSchema(
        window_start=vo.window_start,
        window_end=vo.window_end,
        label=vo.window_key,
        posts=vo.posts,
    )


def map_sf_page_response_vo_to_schema(
    vo: SectionalFeedPageResponseVo,
) -> SfPageResponseSchema:
    """
    Map SectionalFeedPageResponseVo to SfPageResponseSchema.
    """
    return SfPageResponseSchema(
        duration_windows=[
            map_duration_window_vo_to_schema(window)
            for window in vo.duration_windows
        ],
        next_cursor=vo.next_cursor,
        has_more=vo.has_more,
    )
