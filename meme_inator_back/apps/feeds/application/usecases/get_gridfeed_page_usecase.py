import logging
from django.db import DatabaseError
from apps.feeds.application.hydrator import PostHydrator
from apps.feeds.domain.enums.feeds_error_code import FeedsErrorCode
from apps.feeds.domain.irepositories.igridfeed_repository import IGridfeedRepository
from apps.feeds.domain.iusecases.iget_gridfeed_page_usecase import IGetGridfeedPageUsecase
from apps.feeds.domain.entities.gf_page_request_vo import GridfeedPageRequestVo
from apps.feeds.domain.entities.gf_page_response_vo import GridfeedPageResponseVo
from core.results import Error, NotOk, Ok, Result

class GetGridfeedPageUsecase(IGetGridfeedPageUsecase):
    def __init__(
            self, 
            repository: IGridfeedRepository, 
            post_hydrator: PostHydrator
        ):
        self._repository = repository
        self._post_hydrator = post_hydrator

    def execute(self, request_vo: GridfeedPageRequestVo) -> Result[GridfeedPageResponseVo]:
        try:
            # repo result has next_cursor, and raw_posts
            
            repo_result:Result[GridfeedPageResponseVo] = self._repository.fetch_page(request_vo)

            # propagate failure as is
            if not isinstance(repo_result, Ok):
                return repo_result

            # unpack
            raw_posts = repo_result.value.results
            next_cursor = repo_result.value.next_cursor

            # Hydrate posts
            hydrated_posts = self._post_hydrator.hydrate(raw_posts)

            # Wrap in value object
            response_vo = GridfeedPageResponseVo(next_cursor=next_cursor, results=hydrated_posts)
            return Ok(response_vo)
        except (DatabaseError, ConnectionError) as db_exception:
            # logging.exception("Database error in fetch_page")
            return Error("Database error: " + str(db_exception))
        except (ValueError, KeyError, TypeError) as db_exception:
            # logging.exception("Data error in hydration or VO construction")
            return Error(
                message="Data error"+str(db_exception),
                static_msg=FeedsErrorCode.DB_ERROR,
                exception=db_exception,
                status_code=400
            )
        except Exception as e:
            # logging.exception("Unexpected error in GetGridfeedPageUsecase")
            return Error("Unexpected error: " + str(e))