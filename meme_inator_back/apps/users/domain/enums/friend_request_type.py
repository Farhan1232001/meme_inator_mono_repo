from enum import Enum


class FriendRequestType(str, Enum):
    INCOMING = "incoming"
    OUTGOING = "outgoing"