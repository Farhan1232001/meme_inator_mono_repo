from enum import Enum


class PaymentErrorCode(str, Enum):
    """
    Canonical error codes for the Payments domain.

    These values are stable, machine-readable identifiers intended for:
    - API clients
    - observability / analytics
    - idempotent error handling
    """

    # --- Receipt / Validation ---
    INVALID_RECEIPT = "INVALID_RECEIPT"
    RECEIPT_VALIDATION_ERROR = "RECEIPT_VALIDATION_ERROR"
    RECEIPT_USER_MISMATCH = "RECEIPT_USER_MISMATCH"

    # --- Idempotency ---
    IDEMPOTENCY_CONFLICT = "IDEMPOTENCY_CONFLICT"
    DUPLICATE_PROVIDER_TRANSACTION = "DUPLICATE_PROVIDER_TRANSACTION"

    # --- Provider ---
    UNSUPPORTED_PAYMENT_PROVIDER = "UNSUPPORTED_PAYMENT_PROVIDER"
    PROVIDER_COMMUNICATION_ERROR = "PROVIDER_COMMUNICATION_ERROR"

    # --- Fulfillment ---
    FULFILLMENT_FAILED = "FULFILLMENT_FAILED"
    ENTITLEMENT_GRANT_FAILED = "ENTITLEMENT_GRANT_FAILED"
    WALLET_DEPOSIT_FAILED = "WALLET_DEPOSIT_FAILED"

    # --- Access / Authorization ---
    PAYMENT_NOT_OWNED_BY_USER = "PAYMENT_NOT_OWNED_BY_USER"
    SUBSCRIPTION_NOT_ACTIVE = "SUBSCRIPTION_NOT_ACTIVE"

    # --- Fallback ---
    UNKNOWN_PAYMENT_ERROR = "UNKNOWN_PAYMENT_ERROR"
