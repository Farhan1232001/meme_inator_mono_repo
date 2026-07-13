from typing import Any, Dict, List
from uuid import UUID
from django.http import HttpRequest
from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth
from apps.payments.application.dtos.schemas import CoinPurchaseRequest, CoinPurchaseRequestSchema, EntitlementSchema, PaymentSchema, ProductVariantSchema, PurchaseRequest, PurchaseRequestSchema, PurchaseResponseSchema, RestoreRequest, RestoreRequestSchema, RestoreResponseSchema, StripeCheckoutSessionRequest, StripeCheckoutSessionRequestSchema, StripeCheckoutSessionResponseSchema, SubscriptionSchema
from core.dtos.results_schemas import ErrorResponseSchema
from core.dependency_injections import di
from core.results import Result



@api_controller('/payments', tags=['payments'])
class PaymentsController:
    """
    Controller exposing payments endpoints. Each method currently raises NotImplementedError.
    Wire this controller to your routing (Django-Ninja / ninja_extra) and call orchestration methods.
    """

    def __init__(self):
        # adjust DI factory method name to your project's DI module
        self.payments_orchestration = di.create_payments_orchestration()

    # Unified purchase endpoint
    @route.post(
        '/purchase',
        tags=['payments'],
        auth=JWTAuth(),
        permissions=None,
        response={
            200: PurchaseResponseSchema,
            400: ErrorResponseSchema,
            402: ErrorResponseSchema,
            409: ErrorResponseSchema,
        },
    )
    def purchase(self, request: HttpRequest, payload: PurchaseRequestSchema):
        """
        Process a UNIFED purchase; abstracts purchases from different payment providers (Apple IAP, google play store, Stripe). Use Idempotency-Key header for idempotency. Implementation should:
         - read Idempotency-Key from request headers (scoped to user)
         - validate provider payload via payments_orchestration.validate_receipt/usecase
         - check idempotency (idempotency key + provider tx id)
         - persist Payment, grant Entitlement or deposit to wallet, return PurchaseResponse
        """
        # 1. Extract Idempotency-Key
        idempotency_key = request.headers.get('Idempotency-Key')

        # 2. Get user_id. JWTAuth stores it in HttpRequest
        user_id = request.user.id

        if not user_id:
            return 400, ErrorResponseSchema(message="missing authenticated user", static_msg="authentication required")
        
        # ... try to coerce to UUID if it's a string
        if not isinstance(user_id, UUID):
            user_id = UUID(str(user_id))
            return 400, ErrorResponseSchema(message="invalid user id", static_msg="invalid authentication payload")
        
        # 3. Call Orchestration
        purchase_result = self.payments_orchestration.process_purchase(
            user_id = user_id,
            product_sku = payload.product_sku,
            quantity = payload.quantity or 1,
            payment_provider = payload.payment_provider,
            provider_payload = payload.provider_payload.__root__,
            idempotency_key = idempotency_key,
            metadata = payload.metadata,
        )

        # 4. Parse Result
        return Result.result_parser(
            result=purchase_result,
            ok_handler=lambda vo: (
                200,
                PurchaseResponseSchema(
                    idempotency_key=vo.idempotency_key,
                    payment_id=vo.payment_id,
                    provider=vo.provider,
                    provider_transaction_id=vo.provider_transaction_id,
                    original_transaction_id=vo.original_transaction_id,

                    product_sku=vo.product_sku,

                    amount_decimal=vo.amount_decimal,
                    currency=vo.currency,

                    status=vo.status,
                    is_trial=vo.is_trial,

                    purchase_date=vo.purchase_date,
                    expires_date=vo.expires_date,

                    entitlement_granted=vo.entitlement_granted,
                    entitlement_code=vo.entitlement_code,
                    wallet_delta=vo.wallet_delta,
                    subscription=vo.subscription,

                    raw_provider_response=vo.raw_provider_response,
                )
            ),
        )



    # Convenience: buy coin packs
    @route.post(
        '/purchase/coins',
        tags=['payments', 'wallet'],
        auth=JWTAuth(),
        permissions=None,
        response={
            200: PurchaseResponseSchema,
            400: ErrorResponseSchema,
            402: ErrorResponseSchema,
            409: ErrorResponseSchema,
        },
    )
    def purchase_coins(self, payload: CoinPurchaseRequestSchema):
        """
        Convenience endpoint to buy coins. Implementation should:
         - map coin_type / num_of_coins (move these to body if desired)
         - validate provider payload and perform idempotent deposit
        """
        raise NotImplementedError("Implement coin purchase orchestration: validate -> dedupe -> wallet.deposit -> persist")

    # Restore purchases (app-store style)
    @route.post(
        '/restore',
        tags=['payments'],
        auth=JWTAuth(),
        permissions=None,
        response={
            200: RestoreResponseSchema,
            404: ErrorResponseSchema,
            400: ErrorResponseSchema,
        },
    )
    def restore_purchases(self, payload: RestoreRequestSchema):
        """
        Restore subscriptions and non-consumable entitlements from provider receipts.
        Consumables are ignored.
        """
        raise NotImplementedError("Implement RestorePurchasesUsecase: validate -> fetch history -> sync -> return report")

    # Stripe checkout session helper
    @route.post(
        '/stripe/checkout-session',
        tags=['payments'],
        auth=JWTAuth(),
        permissions=None,
        response={
            200: StripeCheckoutSessionResponseSchema,
            400: ErrorResponseSchema,
        },
    )
    def create_stripe_checkout(self, payload: StripeCheckoutSessionRequestSchema):
        """
        Create Stripe Checkout session. Fulfillment still occurs via webhook processing.
        """
        raise NotImplementedError("Implement stripe.checkout session creation via payments provider gateway")

    # User-facing reads
    @route.get(
        '/user/entitlements',
        tags=['payments'],
        auth=JWTAuth(),
        permissions=None,
        response={
            200: List[EntitlementSchema],
        },
    )
    def get_my_entitlements(self):
        """
        Returns entitlements visible to the authenticated user.
        """
        raise NotImplementedError("Implement: call entitlement_service.list_for_user(user_id) and map to EntitlementSchema")

    @route.get(
        '/user/subscriptions',
        tags=['subscriptions'],
        auth=JWTAuth(),
        permissions=None,
        response={
            200: List[SubscriptionSchema],
        },
    )
    def get_my_subscriptions(self):
        """
        Returns subscriptions for the authenticated user.
        """
        raise NotImplementedError("Implement: call subscription_service.list_for_user(user_id) and map to SubscriptionSchema")

    # Product lookup
    @route.get(
        '/products/{product_id}',
        tags=['products'],
        auth=JWTAuth(),
        permissions=None,
        response={
            200: ProductVariantSchema,
            404: ErrorResponseSchema,
        },
    )
    def get_product(self, product_id: str):
        """
        Minimal product info suitable for client display.
        """
        raise NotImplementedError("Implement: fetch ProductVariant by id or internal_sku")

    # Webhook endpoints (no JWT)
    @route.post(
        '/webhooks/stripe',
        tags=['webhooks'],
        auth=None,
        permissions=None,
        response={200: None, 400: ErrorResponseSchema},
    )
    def stripe_webhook(self, body: Dict[str, Any]):
        """
        Stripe webhook receiver (signature validation required).
        """
        raise NotImplementedError("Implement: validate Stripe signature -> parse -> route to HandleWebhookEvent usecase (idempotent)")

    @route.post(
        '/webhooks/apple',
        tags=['webhooks'],
        auth=None,
        permissions=None,
        response={200: None, 400: ErrorResponseSchema},
    )
    def apple_webhook(self, body: Dict[str, Any]):
        """
        Apple App Store Server Notifications (JWS validation).
        """
        raise NotImplementedError("Implement: validate JWS -> parse event -> handle idempotently")

    @route.post(
        '/webhooks/google',
        tags=['webhooks'],
        auth=None,
        permissions=None,
        response={200: None, 400: ErrorResponseSchema},
    )
    def google_webhook(self, body: Dict[str, Any]):
        """
        Google Play RTDN webhook receiver.
        """
        raise NotImplementedError("Implement: validate -> parse -> handle idempotently")

    # Optional: payment detail lookup (owner/admin)
    @route.get(
        '/payments/{payment_id}',
        tags=['payments'],
        auth=JWTAuth(),
        permissions=None,
        response={
            200: PaymentSchema,
            404: ErrorResponseSchema,
        },
    )
    def get_payment(self, payment_id: UUID):
        """
        Retrieve payment detail (owner or admin).
        """
        raise NotImplementedError("Implement: lookup Payment by id and enforce owner/admin access control")