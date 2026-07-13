from typing import Any
from apps.payments.domain.entities.unified_transaction_data_vo import UnifiedTransactionDataVo
from apps.payments.domain.enums.payment_provider_enum import PaymentProviderEnum
from apps.payments.domain.enums.payments_error_codes import PaymentErrorCode
from apps.payments.domain.iusecases.ivalidate_receipt_uc import IValidateReceiptUsecase
from core.results import Error, Ok, Result


class ValidateReceiptUsecase(IValidateReceiptUsecase):
    """
    All receipts NEED to be validated for security reasons. clinet cannot be trusted

    Contact Apple App store (IAP) or Google play store to do server-side check. 
    """
    
    def execute(
        self,
        receipt_data: Any,
        provider: PaymentProviderEnum,
    ) -> Result:
        try:
            unified_tx: UnifiedTransactionDataVo = self.payment_gateway.validate_receipt(
                receipt_data=receipt_data,
                provider=provider,
            )

            return Ok(unified_tx)

        except ValueError as e:
            return Result.NotOk(
                message=str(e),
                static_msg=PaymentErrorCode.INVALID_RECEIPT,
                status_code=400,
            )

        except Exception as e:
            return Error(
                message="Receipt validation failed",
                static_msg=PaymentErrorCode.RECEIPT_VALIDATION_ERROR,
                exception=e,
            )