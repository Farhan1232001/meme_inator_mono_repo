from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from apps.notifications.domain.enums.notification_enum import (
    NotificationType,
    AssociationType,
)


@dataclass
class NotificationEntity:
    notification_id: UUID
    recipient_id: Optional[UUID]
    sender_id: Optional[UUID]

    sender_avatar_url: Optional[str]

    notification_type: NotificationType
    message: str

    is_read: bool
    created_at: datetime

    association_id: Optional[UUID]
    association_type: Optional[AssociationType]

    # -----------------------
    # Domain behaviors
    # -----------------------

    def mark_as_read(self) -> None:
        self.is_read = True

    def is_system_notification(self) -> bool:
        return self.notification_type == NotificationType.SYSTEM_ALERT

    def has_association(self) -> bool:
        return self.association_id is not None and self.association_type is not None
