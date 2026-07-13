import logging
from uuid import UUID
from apps.payments.domain.iusecases.irevoke_entitlement_uc import IRevokeEntitlementUseCase
from apps.payments.domain.iservices.ientitlement_service import IEntitlementService

logger = logging.getLogger(__name__)

class RevokeEntitlementUseCase(IRevokeEntitlementUseCase):
    def __init__(self, entitlement_service: IEntitlementService):
        self.entitlement_service = entitlement_service

    def execute(self, user_id: UUID, codename: str, reason: str) -> None:
        logger.warning(f"Revoking {codename} from {user_id}. Reason: {reason}")
        self.entitlement_service.revoke_entitlement(user_id, codename, reason=reason)