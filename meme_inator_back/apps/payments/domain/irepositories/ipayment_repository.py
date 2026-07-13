from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from payments.domain.entities.payment_entity import PaymentEntity
from payments.domain.enums.payment_provider_enum import PaymentProviderEnum


class IPaymentRepository(ABC):
    @abstractmethod
    def find_by_id(self, payment_id: UUID) -> Optional[PaymentEntity]:
        raise NotImplementedError

    @abstractmethod
    def find_by_provider_transaction_id(
        self,
        provider: PaymentProviderEnum,
        provider_transaction_id: str,
    ) -> Optional[PaymentEntity]:
        """
        Used for idempotency checks.
        """
        raise NotImplementedError

    @abstractmethod
    def save(self, payment: PaymentEntity) -> PaymentEntity:
        raise NotImplementedError

    @abstractmethod
    def update(self, payment: PaymentEntity) -> PaymentEntity:
        raise NotImplementedError
