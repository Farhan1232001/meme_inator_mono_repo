from abc import ABC, abstractmethod
from typing import Any

from apps.payments.domain.entities.unified_transaction_data_vo import UnifiedTransactionDataVo

class ITransactionMapper(ABC):
    """
    A mapper for various Provider specified transaction schemas 
    into a UnifiedTransactionDataVo instance.
    """

    @abstractmethod
    def to_unified_transaction(self, raw_data: Any) -> UnifiedTransactionDataVo:
        """
        Converts provider-specific payload into a unified transaction object.
        """
        pass

# Implementation Examples based on your diagram:



