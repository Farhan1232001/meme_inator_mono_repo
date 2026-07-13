import logging
from typing import Any, Dict
from apps.payments.domain.enums.payments_error_codes import PaymentErrorCode
from apps.payments.domain.iusecases.ifulfill_product_uc import IFulfillPurchaseUsecase
from apps.payments.domain.iservices.ifulfilment_service import IFulfillmentService
from apps.payments.domain.iservices.itransaction_mapper import ITransactionMapper
from core.results import Error, Result

logger = logging.getLogger(__name__)

class FulfillPurchaseUsecase(IFulfillPurchaseUsecase):
    """
    Called after successful payment occurs
    Fulfills purchase by granting entitlement to ProductVariant
    """
    def __init__(
        self, 
        fulfillment_service: IFulfillmentService,
        mappers: Dict[str, ITransactionMapper] # Dict of { 'stripe': StripeMapper(), 'apple': AppleIAPMapper() }
    ):
        self.fulfillment_service = fulfillment_service
        self.mappers = mappers

    def execute(self, provider: str, payload: Dict[str, Any]) -> Result:
        """
        Coordinates the mapping of external events to the internal fulfillment flow.
        """
        logger.info(f"Executing ProcessPaymentEventUseCase for provider: {provider}")

        # 1. Select the appropriate mapper for the provider
        mapper = self.mappers.get(provider.lower())
        
        if not mapper:
            logger.error(f"No mapper configured for payment provider: {provider}")
            return Error(
                message=f'Unsupported payment provider: {provider}',
                static_msg=PaymentErrorCode.UNSUPPORTED_PAYMENT_PROVIDER,
                status_code=422,
                exception=ValueError(f"Unsupported payment provider: {provider}")
            )

        try:
            # 2. Map the raw payload (Dict) to our Domain Value Object (UnifiedTransactionDataVo)
            # Note: You might need to adjust the mapper interface if you pass raw strings vs dicts
            unified_transaction = mapper.to_unified_transaction(payload)
            
            logger.debug(f"Mapped {provider} payload to UnifiedTransactionDataVo for user {unified_transaction.user_id}")

            # 3. Hand off the clean, unified data to the Fulfillment Service
            # This service handles the actual database records and entitlement granting
            self.fulfillment_service.fulfill_purchase(unified_transaction)

        except Exception as e:
            # Payments are CRITICAL, so it is not logged as an exception
            logger.critical(f"Failed to process payment event for {provider}. Error: {str(e)}")
            raise