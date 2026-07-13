from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

from apps.payments.domain.enums.payment_provider_enum import PaymentProviderEnum
from apps.payments.domain.enums.subscription_status_enum import SubscriptionStatusEnum


@dataclass
class SubscriptionEntity:
    """
    TODO: payment providers (like Apple or Google) 
        take a few hours to process a renewal.
    IF user's access expires immediately, 
        they might see "Pay Now" screen while their 
        renewal is actually processing in the background
    """
    # 1. Identity & Ownership
    id: UUID
    user_id: UUID

    # 2. Lifecycle & State
    status: SubscriptionStatusEnum
    product_sku: str

    # 3. Period Timestamps (The 'Access Window')
    current_period_start: datetime
    current_period_end: datetime
    cancel_at_period_end: bool

    # 4. Provider Linking
    provider: PaymentProviderEnum
    provider_subscription_id: str

    def is_active(self) -> bool:
        return True if self.status == SubscriptionStatusEnum.ACTIVE else False

    def extend_period(self, new_end: datetime):
        self.current_period_end = new_end

    def cancel_at_end(self):
        self.cancel_at_period_end = False
    
    def set_cancel_at_end(self, cancel_at_end: bool):
        self.cancel_at_end = cancel_at_end


    def expire(self):
        """Set status is EXPIRED"""
        self.status = SubscriptionStatusEnum.EXPIRED

    def is_expired(self):
        return datetime.now(timezone.utc) > self.current_period_end

    def has_access(self) -> bool:
        """Determines if the user should currently receive premium features."""
        return self.is_active() and not self.is_expired()