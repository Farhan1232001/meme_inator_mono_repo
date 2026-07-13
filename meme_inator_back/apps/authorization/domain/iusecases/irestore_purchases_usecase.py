from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from apps.authorization.domain.entities.entitlement_entity import EntitlementEntity


class IRestorePurchasesUseCase(ABC):
    @abstractmethod
    def execute(self, user_id: UUID, provider: str, receipt_data: str) -> List[EntitlementEntity]:
        ...
