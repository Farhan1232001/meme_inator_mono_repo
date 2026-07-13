from dataclasses import Field
from typing import List, Optional

from pydantic import BaseModel

from apps.notifications.domain.enums.digest_frequency_enum import DigestFrequencyEnum


class CustomDigestPreferencesSchema(BaseModel):
    is_enabled: bool = True
    name: str = "Activity Summary"
    frequency: DigestFrequencyEnum = DigestFrequencyEnum.DAILY
    custom_frequency_in_days: Optional[int] = None
    digest_hour_utc: Optional[int] = Field(None, ge=0, le=23)
    days_of_week: Optional[List[int]] = Field(None, description="0=Monday, 6=Sunday")
    specific_dates: Optional[List[str]] = None  # ISO date strings
    content_types: Optional[List[str]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "is_enabled": True,
                "name": "Your liked Memes Summary",
                "frequency": "daily",
                "custom_frequency_in_days": None,
                "digest_hour_utc": 8,
                "days_of_week": None,
                "specific_dates": None,
                "content_types": ["liked", "commented", "followed"]
            }
        }
