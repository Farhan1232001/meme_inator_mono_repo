from abc import ABC
from typing import Union

from apps.commentsections.domain.entities.comment_content_vo import CommentContentVo
from core.results import Error, Ok, Result


class IValidateCommentContentUsecase(ABC):
    MIN_LENGTH = 1
    MAX_LENGTH = 2000

    def execute(self, raw_text: str) -> Result[CommentContentVo]:
        ...
