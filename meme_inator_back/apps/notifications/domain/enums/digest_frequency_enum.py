from enum import Enum


class DigestFrequencyEnum(str, Enum):
    DAILY = "daily"
    TRIDAILY = "tridaily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"
