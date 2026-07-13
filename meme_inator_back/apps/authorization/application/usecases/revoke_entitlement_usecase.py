from uuid import UUID
from typing import Optional
from apps.authorization.domain.iusecases.irevoke_entitlement_usecase import IRevokeEntitlementUseCase
from apps.authorization.domain.irepositories.iauthorization_repository import IAuthorizationRepository

class RevokeEntitlementUseCase(IRevokeEntitlementUseCase):
    def __init__(self, repository: IAuthorizationRepository):
        self.repository = repository

    def execute(self, user_id: UUID, entitlement_code: str, reason: Optional[str] = None) -> bool:
        # Logic: Find the entitlement and mark it as expired or deleted
        # This prevents the user from accessing premium features immediately
        return self.repository.deactivate_entitlement(user_id, entitlement_code)