from enum import Enum


class FriendRequestAction(str, Enum):
    ACCEPT = "accept"
    REJECT = "reject"