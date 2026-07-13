import logging
from uuid import UUID
from apps.payments.domain.iusecases.igrant_entitlement_uc import IGrantEntitlementUseCase
from apps.payments.domain.iservices.ientitlement_service import IEntitlementService

logger = logging.getLogger(__name__)

class GrantEntitlementUseCase(IGrantEntitlementUseCase):
    def __init__(self, entitlement_service: IEntitlementService):
        self.entitlement_service = entitlement_service

    def execute(self, user_id: UUID, codename: str, source: str) -> None:
        logger.info(f"Granting entitlement {codename} to user {user_id} via {source}")
        self.entitlement_service.grant_entitlement(user_id, codename, source)