from enum import Enum


class AssociationTypeEnum(str, Enum):
    POST = "post"
    COMMENT = "comment"
    PROFILE = "profile"
    TAG = "tag"
    AWARD = "award"
