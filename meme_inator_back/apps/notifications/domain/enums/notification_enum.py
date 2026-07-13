from enum import Enum


class NotificationVerbEnum(str, Enum):
    LIKED = "liked"
    DISLIKED = "disliked"
    COMMENTED = "commented"
    REPLIED = "replied"
    FOLLOWED = "followed"
    MENTIONED = "mentioned"
    SYSTEM_ALERTED = "system_alerted"
    SHARED = "shared"
    AWARDED = "awarded"
    POST_MILESTONED = "post_milestoned"
    FRIEND_REQUESTED = "friend_requested"
    FRIEND_ACCEPTED = "friend_accepted"



