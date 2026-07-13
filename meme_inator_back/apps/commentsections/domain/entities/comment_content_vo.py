
from dataclasses import dataclass, field
from pydantic import ValidationError

from core.results import Error, NotOk, Ok, Result


@dataclass
class CommentContentVo:
    text: str
    MIN_LENGTH = 1
    MAX_LENGTH: int = field(default=2000, init=False)

    def validate_length(self) -> Result:
        """
        Validates string to see if its withing its char length (0, 2000]
        """
        if self.text is None:
            return NotOk(
                message="Comment content is required",
                static_msg="comment.content.required",
                status_code=400,
            )

        text = self.text.strip()

        if not self.text:
            return NotOk(
                message="Comment cannot be empty",
                static_msg="comment.content.empty",
                status_code=400,
            )

        if len(self.text) < self.MIN_LENGTH:
            return NotOk(
                message="Comment is too short",
                static_msg="comment.content.too_short",
                status_code=400,
            )

        if len(self.text) > self.MAX_LENGTH:
            return NotOk(
                message="Comment is too long",
                static_msg="comment.content.too_long",
                status_code=400,
            )

        return Ok(value='Comment Created Successfully')
