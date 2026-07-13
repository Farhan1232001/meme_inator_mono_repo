from abc import ABC, abstractmethod
from uuid import UUID

from apps.payments.domain.entities.unified_transaction_data_vo import UnifiedTransactionDataVo
from apps.payments.domain.enums.payment_provider_enum import PaymentProviderEnum

class IValidateReceiptUsecase(ABC):
    """
    All receipts NEED to be validated for security reasons. clinet cannot be trusted

    Contact Apple App store (IAP) or Google play store to do server-side check. 
    """
    @abstractmethod
    def execute(self, receipt_data: str, provider: PaymentProviderEnum) -> UnifiedTransactionDataVo:
        ...