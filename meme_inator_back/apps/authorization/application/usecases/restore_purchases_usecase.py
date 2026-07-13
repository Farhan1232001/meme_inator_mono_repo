from typing import List
from uuid import UUID
from apps.authorization.domain.entities.entitlement_entity import EntitlementEntity
from apps.authorization.domain.irepositories.iauthorization_repository import IAuthorizationRepository
from apps.authorization.domain.iusecases.irestore_purchases_usecase import IRestorePurchasesUseCase


class RestorePurchasesUseCase(IRestorePurchasesUseCase):
    def __init__(self, repository: IAuthorizationRepository):
        self.repository = repository

    def execute(self, user_id: UUID, provider: str, receipt_data: str) -> List[EntitlementEntity]:
        # Here you would typically call an external service (Apple/Google)
        # and then update the repository
        # For now, we fetch current active ones
        return self.repository.get_active_entitlements(user_id)