from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from apps.payments.domain.entities.money_vo import MoneyVo
from apps.payments.domain.enums.payment_provider_enum import PaymentProviderEnum
from apps.payments.domain.enums.payment_status_enum import PaymentStatusEnum


@dataclass
class PaymentEntity:
    # 1. Identity & Ownership
    id: UUID
    user_id: UUID

    # 2. Financial Data
    money: MoneyVo
    status: PaymentStatusEnum

    # 3. Provider Linking (For Idempotency & Troubleshooting)
    provider: PaymentProviderEnum
    provider_transaction_id: str
    provider_original_id: Optional[str]

    # 4. Product Metadata
    product_sku: str

    # 5. Audit Timestamp
    created_at: datetime

    def mark_as_succeeded(self):
        self.status = PaymentStatusEnum.SUCCEEDED

    def mark_as_failed(self, reason: str):
        self.status = PaymentStatusEnum.FAILED
        # TODO: Log Error

    def mark_as_refunded(self):
        """Payment status is set to REFUNDED status ONLY IF previous status is SUCCEEDED"""
        if self.status == PaymentStatusEnum.SUCCEEDED:
            self.status = PaymentStatusEnum.REFUNDED
