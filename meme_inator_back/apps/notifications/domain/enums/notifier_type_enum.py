from enum import Enum


class NotifierTypeEnum(str, Enum):
    SYS = "sys"
    USER = "user"
    ADMIN = "admin"
    SERVICE = "service"