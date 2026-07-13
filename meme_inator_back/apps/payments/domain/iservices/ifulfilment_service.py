# domain/iusecases/ifulfilment_service.py
from abc import ABC, abstractmethod

from domain.entities.unified_transaction_data_vo import UnifiedTransactionDataVo


class IFulfillmentService(ABC):
    """
    Responsibilities
    1.  Coordinates fulfillment after a successful payment.
        Decides which downstream domain service to invoke based on ProductType.

    2. Attempt Restoration for payments

    """

    @abstractmethod
    def fulfill_purchase(self, transaction: UnifiedTransactionDataVo) -> None:
        ...
