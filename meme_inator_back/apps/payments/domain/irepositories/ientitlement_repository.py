from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from payments.domain.entities.entitlement_entity import EntitlementEntity


class IEntitlementRepository(ABC):
    @abstractmethod
    def find_by_user_and_codename(
        self,
        user_id: UUID,
        codename: str,
    ) -> Optional[EntitlementEntity]:
        raise NotImplementedError

    @abstractmethod
    def grant(self, entitlement: EntitlementEntity) -> EntitlementEntity:
        raise NotImplementedError

    @abstractmethod
    def revoke(self, user_id: UUID, codename: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, entitlement: EntitlementEntity) -> EntitlementEntity:
        raise NotImplementedError
