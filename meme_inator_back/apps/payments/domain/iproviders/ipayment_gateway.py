# domain/irepositories/ipayment_gateway.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Any
from uuid import UUID

from apps.payments.domain.entities.unified_transaction_data_vo import UnifiedTransactionDataVo

# forward-referenced return types (replace with your actual classes if desired):
# - "ExternalTransactionData" : standardized data returned by mobile receipt validation
# - "UnifiedEvent" : internal event representation created from provider webhooks

class IPaymentGateway(ABC):
    """
    Abstract interface for payment gateway adapters (Stripe, Apple IAP, Google Play, etc).

    Implementations should:
    - normalize provider-specific responses into project VOs (e.g. ExternalTransactionData).
    - raise domain.exceptions.InvalidReceiptException when a receipt/token is invalid.
    """

    @abstractmethod
    def validate_receipt(self, receipt_data: str) -> UnifiedTransactionDataVo:
        """
        Validate a mobile receipt / token with its provider (App Store, Google Play).
        Returns a standardized ExternalTransactionData object.

        Raises:
            InvalidReceiptException: if the receipt/token is invalid or cannot be verified.
        """
        ...

    @abstractmethod
    def create_checkout_session(self, internal_sku: str, user_id: UUID) -> str:
        """
        For hosted checkout providers (e.g. Stripe), create a checkout/payment session
        and return the URL the user should visit to complete payment.

        Returns:
            str: URL for user to complete payment (checkout session URL).
        """
        ...

    # Methods used by BOTH mobile payment providers and stripe

    @abstractmethod
    def get_subscription_details(self, subscription_id: str) -> Dict[str, Any]:
        """
        Fetch the current status/details of a subscription from the payment provider.

        Returns:
            dict: provider-specific subscription details (implementations may map to a VO).
        """
        ...

    @abstractmethod
    def parse_webhook_event(self, payload: Dict[str, Any], signature: str) -> "UnifiedEvent":
        """
        Convert provider webhook JSON + signature into a standardized internal event
        (e.g. PAYMENT_SUCCEEDED, SUBSCRIPTION_RENEWED).

        Implementations must:
        - validate the signature
        - map provider-specific event types to the internal UnifiedEvent representation
        """
        ...
