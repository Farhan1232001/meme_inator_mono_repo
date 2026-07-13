from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID
from ninja import Schema

class ProviderPayloadSchema(Schema):
    # provider-specific blob - kept free-form
    __root__: Optional[Dict[str, Any]] = None


class PurchaseRequestSchema(Schema):
    product_sku: str
    quantity: Optional[int] = 1
    payment_provider: str
    provider_payload: ProviderPayloadSchema
    metadata: Optional[Dict[str, Any]] = None


class CoinPurchaseRequestSchema(Schema):
    payment_provider: str
    provider_payload: ProviderPayloadSchema
    client_reference: Optional[str] = None


class StripeCheckoutSessionRequestSchema(Schema):
    product_sku: str
    success_url: str
    cancel_url: str
    metadata: Optional[Dict[str, Any]] = None


class StripeCheckoutSessionResponseSchema(Schema):
    session_id: Optional[str] = None
    checkout_url: Optional[str] = None


class PurchaseResponseSchema(Schema):
    # Identity & Idempotency
    idempotency_key: Optional[str] = None
    payment_id: UUID
    provider: str
    provider_transaction_id: str
    original_transaction_id: Optional[str] = None

    # Product & Pricing
    amount_decimal: float
    currency: str

    # Lifecycle
    status: str
    is_trial: Optional[bool] = False

    # Timestamps
    purchase_date: datetime
    expires_date: Optional[datetime] = None

    # Fulfillment
    entitlement_granted: Optional[bool] = False
    entitlement_code: Optional[str] = None
    wallet_delta: Optional[int] = None
    subscription: Optional[Dict[str, Any]] = None

    # Debug
    raw_provider_response: Optional[Dict[str, Any]] = None


class RestoreRequestSchema(Schema):
    payment_provider: str
    provider_payload: ProviderPayloadSchema


class RestoreResponseSchema(Schema):
    restored_entitlements: Optional[List[Dict[str, Any]]] = None
    restored_subscriptions: Optional[List[Dict[str, Any]]] = None


class EntitlementSchema(Schema):
    codename: str
    granted_at: datetime
    expires_at: Optional[datetime] = None
    source: Optional[str] = None


class SubscriptionSchema(Schema):
    id: UUID
    product_sku: str
    status: str
    current_period_start: datetime
    current_period_end: datetime
    cancel_at_period_end: bool
    provider_subscription_id: Optional[str] = None


class ProductVariantSchema(Schema):
    id: UUID
    internal_sku: str
    product_type: str
    provider_mappings: Optional[Dict[str, Any]] = None
    entitlement_codename: Optional[str] = None
    token_grants_amount: Optional[int] = None


class PaymentSchema(Schema):
    id: UUID
    user_id: UUID
    provider: str
    provider_transaction_id: str
    product_sku: str
    amount_cents: int
    currency: str
    status: str
    created_at: datetime


class ErrorResponseSchema(Schema):
    detail: Optional[str] = None
    code: Optional[str] = None
    message: Optional[str] = None
    static_msg: Optional[str] = None
    exception_str: Optional[str] = None
