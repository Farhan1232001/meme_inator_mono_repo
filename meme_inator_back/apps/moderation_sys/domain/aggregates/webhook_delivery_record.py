from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
from enum import Enum

from apps.moderation_sys.domain.aggregates.policy_definition import PolicyDefinition


class DeliveryStatus(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    EXPIRED = "expired"




@dataclass
class WebhookDeliveryRecord:
    """Aggregate Root for webhook delivery records"""
    policy_definition: PolicyDefinition
    status: DeliveryStatus = field(default=DeliveryStatus.PENDING)
    retry_count: int = field(default=0)
    created_at: datetime = field(default_factory=datetime.now)
    last_retry_at: Optional[datetime] = field(default=None)
    expires_at: Optional[datetime] = field(default=None)

    def schedule_delivery(self) -> None:
        """Schedule the delivery"""
        self.status = DeliveryStatus.PENDING
        self.expires_at = datetime.now() + timedelta(hours=24)

    def mark_success(self) -> None:
        """Mark the delivery as successful"""
        self.status = DeliveryStatus.SUCCESS

    def mark_failure(self, max_retries: int = 5) -> None:
        """Mark the delivery as failed and update retry count"""
        self.retry_count += 1
        if self.retry_count >= max_retries:
            self.status = DeliveryStatus.FAILED
        self.last_retry_at = datetime.now()

    def expire(self) -> None:
        """Mark the delivery as expired"""
        self.status = DeliveryStatus.EXPIRED
        self.expires_at = datetime.now()

    def is_ready_for_retry(self) -> bool:
        """Check if the delivery is ready for retry"""
        if self.status != DeliveryStatus.PENDING:
            return False
        if self.expires_at and datetime.now() > self.expires_at:
            self.expire()
            return False
        return True
