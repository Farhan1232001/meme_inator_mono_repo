from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from apps.payments.domain.enums.payment_provider_enum import PaymentProviderEnum
from apps.payments.domain.enums.payment_status_enum import PaymentStatusEnum


@dataclass(frozen=True)
class UnifiedTransactionDataVo:
    """
    Generic transaction value object that is payment provider agnostic. 

    NOTE: Transaction instance is time agnostic.
        that means that This class can represent transactions that have already occured or will occur.
        ex. Mobile store fronts compute transaction on their servers, then a receipt
        is sent here for tracking purposes. 
    """
    # 1. Identity & Idempotency
    provider: PaymentProviderEnum
    provider_transaction_id: str

    # 2. The "chain of history" (critical for subscriptions)
    # This links a renewal back to the first time the user ever paid. 
    # Apple: originalTransactionId | Google: linkedPurchaseToken | Stripe: subscription_id
    original_transaction_id: Optional[str] = None

    # 3. Product & Pricing
    product_id: str
    amount_decimal: float
    currency: str   # USD, etc

    # 4. Status & 
    # Normalize these so your Orchestrator doesn't have to speak 3 languages.
    status: PaymentStatusEnum #  # SUCCEEDED, PENDING, REFUNDED, FAILED
    is_trial: bool

    # 5. Timestamps
    purchase_date: datetime
    # ... Crucial for Sync: When does this specific period end?    expires_date: Optional[datetime]
    expires_date: Optional[datetime] = None

    # 6. metadata & envionrment
    user_id: UUID
    environment: str
    raw_response: Dict[str, Any] # the full JSON for debugging

    def is_successful(self) -> bool:
        return True if self.status == 'SUCCEEDED' else False

    def get_unique_lookup_key(self) -> str:
        """
        Returns a composite key to uniquely identify a transaction across all providers.
        Format: {provider}:{provider_transaction_id}
        """
        return f"{self.provider.value}:{self.provider_transaction_id}"