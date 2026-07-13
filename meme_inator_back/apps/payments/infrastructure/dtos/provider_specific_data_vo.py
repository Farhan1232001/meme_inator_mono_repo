from dataclasses import dataclass
from typing import Any, Dict, Optional

from apps.payments.domain.enums.payment_provider_enum import PaymentProviderEnum


@dataclass
class ProviderSpecificReceiptData:
    provider: PaymentProviderEnum
    raw_payload: Dict[str, Any]
    signature: Optional[str] = None
