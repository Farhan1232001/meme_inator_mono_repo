from enum import Enum


class VoteActionEnum(str, Enum):
    UPVOTE = "upvote"
    DOWNVOTE = "downvote"
    REMOVE_UPVOTE = "remove_upvote"
    REMOVE_DOWNVOTE = "remove_downvote"

    @classmethod
    def to_dict(cls):
        return {action.name: action.value for action in cls}