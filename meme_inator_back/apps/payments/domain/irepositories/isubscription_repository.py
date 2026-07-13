from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from payments.domain.entities.subscription_entity import SubscriptionEntity
from payments.domain.enums.payment_provider_enum import PaymentProviderEnum


class ISubscriptionRepository(ABC):
    @abstractmethod
    def find_by_id(self, subscription_id: UUID) -> Optional[SubscriptionEntity]:
        raise NotImplementedError

    @abstractmethod
    def find_by_provider_subscription_id(
        self,
        provider: PaymentProviderEnum,
        provider_subscription_id: str,
    ) -> Optional[SubscriptionEntity]:
        raise NotImplementedError

    @abstractmethod
    def find_active_by_user_and_sku(
        self,
        user_id: UUID,
        product_sku: str,
    ) -> Optional[SubscriptionEntity]:
        raise NotImplementedError

    @abstractmethod
    def save(self, subscription: SubscriptionEntity) -> SubscriptionEntity:
        raise NotImplementedError

    @abstractmethod
    def update(self, subscription: SubscriptionEntity) -> SubscriptionEntity:
        raise NotImplementedError
