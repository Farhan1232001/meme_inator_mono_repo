
from enum import Enum


class VoteTypeEnum(str, Enum):
    UPVOTE = "upvote"
    DOWNVOTE = "downvote"