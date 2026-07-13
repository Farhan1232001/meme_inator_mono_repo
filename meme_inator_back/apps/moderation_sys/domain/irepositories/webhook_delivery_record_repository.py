# domain/irepositories/webhook_delivery_record_repository.py
from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional, List
from datetime import datetime

from apps.moderation_sys.domain.aggregates.webhook_delivery_record import WebhookDeliveryRecord

class IWebhookDeliveryRecordRepository(ABC):
    @abstractmethod
    def save(self, record: WebhookDeliveryRecord) -> WebhookDeliveryRecord:
        """Save or update a webhook delivery record"""
        pass

    @abstractmethod
    def find_by_id(self, record_id: UUID) -> Optional[WebhookDeliveryRecord]:
        """Find webhook delivery record by ID"""
        pass

    @abstractmethod
    def find_failed_ready_for_retry(self, limit: int = 100) -> List[WebhookDeliveryRecord]:
        """Find failed records that are ready for retry"""
        pass

    @abstractmethod
    def find_by_status(self, status: str, limit: int = 100) -> List[WebhookDeliveryRecord]:
        """Find records by delivery status"""
        pass

    @abstractmethod
    def find_expired(self) -> List[WebhookDeliveryRecord]:
        """Find expired records that haven't been delivered"""
        pass

    @abstractmethod
    def find_by_case_id(self, case_id: UUID) -> List[WebhookDeliveryRecord]:
        """Find all webhook deliveries for a specific moderation case"""
        pass

    @abstractmethod
    def mark_as_expired(self, older_than: datetime) -> int:
        """Mark old pending records as expired, returns count updated"""
        pass