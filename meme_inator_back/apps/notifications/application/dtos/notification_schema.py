from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from apps.notifications.application.dtos.notification_payload_schema import NotificationPayloadSchema
from apps.notifications.application.dtos.notifier_schema import NotifierSchema
from apps.notifications.domain.enums.association_type_enum import AssociationTypeEnum
from apps.notifications.domain.enums.channel_type_enum import ChannelTypeEnum
from apps.notifications.domain.enums.notification_enum import NotificationVerbEnum


class NotificationSchema(BaseModel):
    id: UUID
    sender: NotifierSchema
    sender_avatar_url: Optional[str] = None
    recipient_id: UUID
    notification_verb: NotificationVerbEnum
    message: str
    is_read: bool
    read_at: Optional[datetime] = None
    created_at: datetime
    is_public: bool = False
    association_id: Optional[UUID] = None
    association_type: Optional[AssociationTypeEnum] = None
    payload: Optional[NotificationPayloadSchema] = None
    channel_type: Optional[ChannelTypeEnum] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "sender": {
                    "id": "223e4567-e89b-12d3-a456-426614174000",
                    "type": "user",
                    "service_name": None
                },
                "sender_avatar_url": "https://example.com/avatar.jpg",
                "recipient_id": "323e4567-e89b-12d3-a456-426614174000",
                "notification_verb": "liked",
                "message": "John liked your post",
                "is_read": False,
                "read_at": None,
                "created_at": "2024-01-15T10:30:00Z",
                "is_public": False,
                "association_id": "423e4567-e89b-12d3-a456-426614174000",
                "association_type": "post",
                "channel_type": "in_app"
            }
        }

