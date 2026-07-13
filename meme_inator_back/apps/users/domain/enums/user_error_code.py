from enum import Enum

class UserErrorCode(str, Enum):
    USER_NOT_FOUND = "USER_NOT_FOUND"
    USER_BANNED = "USER_BANNED"
