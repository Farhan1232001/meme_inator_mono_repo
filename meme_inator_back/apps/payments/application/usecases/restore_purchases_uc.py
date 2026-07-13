# application/usecases/restore_purchases_uc.py
import logging
from uuid import UUID
from typing import List

from apps.payments.domain.iusecases.irestore_purchases_uc import IRestorePurchasesUseCase
from apps.payments.domain.irepositories.ipayment_repository import IPaymentRepository
from apps.payments.domain.iservices.ifulfilment_service import IFulfillmentService # Only depends on this!
from apps.payments.domain.enums.payment_status_enum import PaymentStatusEnum

logger = logging.getLogger(__name__)

class RestorePurchasesUseCase(IRestorePurchasesUseCase):
    def __init__(
        self, 
        payment_repo: IPaymentRepository,
        fulfillment_service: IFulfillmentService
    ):
        self.payment_repo = payment_repo
        self.fulfillment_service = fulfillment_service

    def execute(self, user_id: UUID) -> None:
        logger.info(f"Starting purchase restoration for user {user_id}")
        
        # 1. Get History
        # We assume find_by_user_id returns a list of PaymentEntity
        all_payments = self.payment_repo.find_by_user_id(user_id)
        
        successful_payments = [
            p for p in all_payments 
            if p.status == PaymentStatusEnum.COMPLETED
        ]

        if not successful_payments:
            logger.info(f"No successful payment history found for user {user_id}")
            return

        restored_count = 0

        # 2. Delegate "Thinking" to the Service
        for payment in successful_payments:
            try:
                # The service decides IF it should be restored and HOW
                was_restored = self.fulfillment_service.attempt_restoration(payment)
                
                if was_restored:
                    restored_count += 1
            
            except Exception as e:
                logger.error(f"Error restoring payment {payment.id}: {str(e)}")

        logger.info(f"Restoration complete. Refreshed {restored_count} entitlements for user {user_id}")