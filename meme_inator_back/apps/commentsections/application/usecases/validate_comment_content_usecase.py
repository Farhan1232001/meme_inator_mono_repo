from typing import Union

from apps.commentsections.domain.entities.comment_content_vo import CommentContentVo
from apps.commentsections.domain.iusecases.ivalidate_comment_content_usecase import IValidateCommentContentUsecase
from core.results import Error, Ok, Result


class ValidateCommentContentUsecase(IValidateCommentContentUsecase):
    MIN_LENGTH = 1
    MAX_LENGTH = 2000

    def execute(self, raw_text: str) -> Result[CommentContentVo]:
        comment_content_vo: CommentContentVo = CommentContentVo(raw_text)

        # Ok result will contain CommentContentVo as its value
        validated_comment_content_vo:Result[str] = comment_content_vo.validate_length()

        return validated_comment_content_vo
