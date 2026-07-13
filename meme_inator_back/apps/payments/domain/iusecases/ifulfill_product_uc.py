from abc import ABC, abstractmethod
from typing import Any, Dict

class IFulfillPurchaseUsecase(ABC):
    """
    fulfills purchase by granting entitlement to ProductVariant
    """
    @abstractmethod
    def execute(self, provider: str, payload: Dict[str, Any]) -> None:
        ...