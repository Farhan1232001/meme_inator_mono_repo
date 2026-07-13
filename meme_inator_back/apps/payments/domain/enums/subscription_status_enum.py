from enum import Enum


class SubscriptionStatusEnum(str, Enum):
    ACTIVE = "ACTIVE"
    PAST_DUE = "PAST_DUE"
    CANCELED = "CANCELED"
    EXPIRED = "EXPIRED"
    TRIALING = "TRIALING"