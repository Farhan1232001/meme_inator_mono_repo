

from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from apps.notifications.domain.enums.notifier_type_enum import NotifierTypeEnum


class NotifierSchema(BaseModel):
    id: UUID
    type: NotifierTypeEnum
    service_name: Optional[str] = None # which service is notifing? a moderation bot? newsletter engine? recomendation engine?, etc

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "type": "user",
                "service_name": None
            }
        }

    def is_user(self) -> bool:
        return self.type == NotifierTypeEnum.USER

    def is_system(self) -> bool:
        return self.type == NotifierTypeEnum.SYS

    def is_service(self) -> Optional[str]:
        return self.service_name if self.type == NotifierTypeEnum.SERVICE else None