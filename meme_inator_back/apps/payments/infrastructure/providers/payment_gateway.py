# infrastructure/providers/payment_gateway_impl.py
from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID
from typing import Dict, Any
import uuid

from apps.payments.domain.entities.unified_transaction_data_vo import UnifiedTransactionDataVo
from apps.payments.domain.enums.payment_provider_enum import PaymentProviderEnum
from apps.payments.domain.enums.payment_status_enum import PaymentStatusEnum
from apps.payments.domain.iproviders.ipayment_gateway import IPaymentGateway
from core.results import Error


class DefaultPaymentGateway(IPaymentGateway):
    """
    Base/default payment gateway. You can subclass per provider for more complex logic.
    """

    def validate_receipt(
        self,
        receipt_data: Dict[str, Any],
        provider: PaymentProviderEnum,
    ) -> UnifiedTransactionDataVo | Error:
        """
        Validates a receipt with the provider.
        Returns a fully normalized UnifiedTransactionDataVo or an Error object.
        """
        try:
            if provider == PaymentProviderEnum.APPLE_IAP:
                return self._validate_receipt_apple_iap(receipt_data)
            elif provider == PaymentProviderEnum.GOOGLE_PLAY:
                return self._validate_receipt_google(receipt_data)
            elif provider == PaymentProviderEnum.STRIPE:
                return self._validate_receipt_stripe(receipt_data)
            else:
                return Error(
                    message=f"Unsupported provider: {provider}",
                    static_msg="UNSUPPORTED_PROVIDER",
                    status_code=400
                )
        except Exception as exc:
            return Error(
                message="Receipt validation failed",
                static_msg="VALIDATION_ERROR",
                status_code=400,
                exception=exc
            )

    # -------------------------------------------------------------------------
    # Apple IAP validation
    # -------------------------------------------------------------------------
    def _validate_receipt_apple_iap(self, payload: Dict[str, Any]) -> UnifiedTransactionDataVo | Error:
        """
        Stub implementation for Apple IAP receipt validation.
        In production, call Apple verification endpoint and parse the response.
        """
        try:
            # Example: simulate Apple server response
            # TODO: Replace with real Apple verification call
            apple_response = payload.get("receipt") or {}  # fake response

            if not apple_response:
                return Error(
                    message="Empty Apple receipt",
                    static_msg="EMPTY_RECEIPT",
                    status_code=400
                )

            # Map Apple receipt to UnifiedTransactionDataVo
            return UnifiedTransactionDataVo(
                provider=PaymentProviderEnum.APPLE_IAP,
                provider_transaction_id=str(apple_response.get("transaction_id", uuid.uuid4())),
                original_transaction_id=apple_response.get("original_transaction_id"),
                product_id=apple_response.get("product_id", "unknown"),
                amount_decimal=float(apple_response.get("amount", 0.0)),
                currency=apple_response.get("currency", "USD"),
                status=PaymentStatusEnum.SUCCEEDED,
                is_trial=apple_response.get("is_trial_period", False),
                purchase_date=apple_response.get("purchase_date", datetime.now(timezone.utc)),
                expires_date=apple_response.get("expires_date"),
                user_id=UUID(apple_response.get("user_id", str(uuid.uuid4()))),
                environment=apple_response.get("environment", "sandbox"),
                raw_response=apple_response
            )

        except Exception as exc:
            return Error(
                message="Apple receipt validation failed",
                static_msg="APPLE_VALIDATION_ERROR",
                status_code=400,
                exception=exc
            )

    # -------------------------------------------------------------------------
    # Google Play stub
    # -------------------------------------------------------------------------
    def _validate_receipt_google(self, payload: Dict[str, Any]) -> Error:
        return Error(
            message="Google receipt validation not implemented",
            static_msg="GOOGLE_VALIDATION_NOT_IMPLEMENTED",
            status_code=501
        )

    # -------------------------------------------------------------------------
    # Stripe stub
    # -------------------------------------------------------------------------
    def _validate_receipt_stripe(self, payload: Dict[str, Any]) -> Error:
        return Error(
            message="Stripe receipt validation not implemented",
            static_msg="STRIPE_VALIDATION_NOT_IMPLEMENTED",
            status_code=501
        )
