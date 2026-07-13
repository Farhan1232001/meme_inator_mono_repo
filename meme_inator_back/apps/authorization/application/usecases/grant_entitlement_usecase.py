from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID
from apps.authorization.domain.entities.entitlement_entity import EntitlementEntity
from apps.authorization.domain.irepositories.iauthorization_repository import IAuthorizationRepository
from apps.authorization.domain.iusecases.igrant_entitlement_usecase import IGrantEntitlementUseCase


class GrantEntitlementUseCase(IGrantEntitlementUseCase):
    def __init__(self, repository: IAuthorizationRepository):
        self.repository = repository

    def execute(self, user_id: UUID, entitlement_code: str, expires_at: Optional[datetime], source: str, meta: Optional[Dict[str, Any]] = None) -> EntitlementEntity:
        # Validates if entitlement exists and saves it
        return self.repository.create_user_entitlement(
            user_id=user_id,
            code=entitlement_code,
            expires_at=expires_at,
            source=source,
            meta=meta or {}
        )