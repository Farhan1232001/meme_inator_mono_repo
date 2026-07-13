from enum import Enum


class PostVoteTypeEnum(str, Enum):
    UPVOTE = 'upvote'
    DOWNVOTE = 'downvote'