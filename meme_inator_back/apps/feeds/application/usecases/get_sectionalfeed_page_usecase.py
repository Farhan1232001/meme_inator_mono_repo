# apps/feeds/application/usecases/get_sectionalfeed_page_usecase.py
import logging
from django.db import DatabaseError

from apps.feeds.application.hydrator import PostHydrator
from apps.feeds.domain.enums.feeds_error_code import FeedsErrorCode
from apps.feeds.domain.irepositories.isectionalfeed_respository import ISectionalfeedRepository
from apps.feeds.domain.iusecases.iget_sectionalfeed_page_usecase import (
    IGetSectionalfeedPageUsecase
)
from apps.feeds.domain.entities.sf_page_request_vo import SectionalFeedPageRequestVo
from apps.feeds.domain.entities.sf_page_response_vo import SectionalFeedPageResponseVo
from apps.feeds.domain.entities.duration_window_vo import DurationWindow
from core.results import Result, Ok, Error


class GetSectionalfeedPageUsecase(IGetSectionalfeedPageUsecase):
    def __init__(
        self,
        repository: ISectionalfeedRepository,
        post_hydrator: PostHydrator,
    ):
        self._repository = repository
        self._post_hydrator = post_hydrator

    def execute(
        self,
        request_vo: SectionalFeedPageRequestVo
    ) -> Result[SectionalFeedPageResponseVo]:
        try:
            # Repository returns Result[SectionalFeedResponseVo]
            sfResponseVoResult: Result[SectionalFeedPageResponseVo] = (
                self._repository.fetch_page(request_vo)
            )

            # Propagate failure as-is
            if not isinstance(sfResponseVoResult, Ok):
                return sfResponseVoResult

            sfResponseVo = sfResponseVoResult.value

            # Hydrate posts in-place (efficient)
            # Mutating a value object (vo) is wrong but this is more efficient
            for window in sfResponseVo.duration_windows:
                self._post_hydrator.hydrate(window.posts)

            return Ok(sfResponseVo)

        except (DatabaseError, ConnectionError) as db_exception:
            return Error("Database error: " + str(db_exception))

        except (ValueError, KeyError, TypeError) as data_exception:
            return Error(
                message="Data error: " + str(data_exception),
                static_msg=FeedsErrorCode.DB_ERROR,
                exception=data_exception,
                status_code=400
            )


        except Exception as e:
            return Error("Unexpected error: " + str(e))
