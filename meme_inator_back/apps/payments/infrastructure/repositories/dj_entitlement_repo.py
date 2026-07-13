from typing import Optional
from uuid import UUID

from payments.domain.entities.entitlement_entity import EntitlementEntity
from payments.domain.irepositories.ientitlement_repository import IEntitlementRepository
from payments.infrastructure.models.entitlement_model import EntitlementModel


class DjangoEntitlementRepository(IEntitlementRepository):

    def find_by_user_and_codename(
        self,
        user_id: UUID,
        codename: str,
    ) -> Optional[EntitlementEntity]:
        model = EntitlementModel.objects.filter(
            user_id=user_id,
            codename=codename,
        ).first()

        return self._to_entity(model) if model else None

    def grant(self, entitlement: EntitlementEntity) -> EntitlementEntity:
        model = EntitlementModel.objects.create(
            user_id=entitlement.user_id,
            codename=entitlement.codename,
            granted_at=entitlement.granted_at,
            expires_at=entitlement.expires_at,
            source=entitlement.source,
        )
        return self._to_entity(model)

    def revoke(self, user_id: UUID, codename: str) -> None:
        EntitlementModel.objects.filter(
            user_id=user_id,
            codename=codename,
        ).delete()

    def update(self, entitlement: EntitlementEntity) -> EntitlementEntity:
        EntitlementModel.objects.filter(
            user_id=entitlement.user_id,
            codename=entitlement.codename,
        ).update(
            expires_at=entitlement.expires_at,
        )
        return self.find_by_user_and_codename(
            entitlement.user_id,
            entitlement.codename,
        )

    def _to_entity(self, model: EntitlementModel) -> EntitlementEntity:
        return EntitlementEntity(
            user_id=model.user_id,
            codename=model.codename,
            granted_at=model.granted_at,
            expires_at=model.expires_at,
            source=model.source,
        )
