from typing import Any, Dict, Optional
from uuid import UUID

from apps.payments.domain.entities.unified_transaction_data_vo import UnifiedTransactionDataVo
from apps.payments.domain.iproviders.ipayment_gateway import IPaymentGateway
from apps.payments.domain.iservices.itransaction_mapper import ITransactionMapper
from apps.payments.domain.iusecases.ifulfill_product_uc import IFulfillPurchaseUsecase
from apps.payments.domain.iusecases.igrant_entitlement_uc import IGrantEntitlementUseCase
from apps.payments.domain.iusecases.irestore_purchases_uc import IRestorePurchasesUseCase
from apps.payments.domain.iusecases.irevoke_entitlement_uc import IRevokeEntitlementUseCase
from apps.payments.domain.iusecases.ivalidate_receipt_uc import IValidateReceiptUsecase
from core.results import Ok, Result


class PaymentsOrchestration:
    """
    Orchestrator / traffic-control for payment flows.

    This class is intentionally a thin coordination layer. Inject real use-cases,
    repositories and gateway adapters at construction time. All public methods
    raise NotImplementedError as boilerplate for you to implement business logic.
    """

    def __init__(
        self,
        payment_gateway: IPaymentGateway,
        fulfill_product_uc: IFulfillPurchaseUsecase,
        grant_entitlement_uc: IGrantEntitlementUseCase,
        restore_purchases_uc: IRestorePurchasesUseCase,
        revoke_entitlement_uc: IRevokeEntitlementUseCase,
        validate_receipt_uc: IValidateReceiptUsecase,
        transaction_mapper: ITransactionMapper,
    ):
        # store dependencies so implementor can use them
        self.payment_gateway = payment_gateway
        self.fulfill_product_uc = fulfill_product_uc
        self.grant_entitlement_uc = grant_entitlement_uc
        self.restore_purchases_uc = restore_purchases_uc
        self.revoke_entitlement_uc = revoke_entitlement_uc
        self.validate_receipt_uc = validate_receipt_uc
        self.transaction_mapper = transaction_mapper
        
    # ---------------------------------------------------------------------
    # Purchase flows
    # ---------------------------------------------------------------------

    def process_purchase(
        self,
        *,
        user_id: UUID,
        product_sku: str,
        quantity: int,
        payment_provider: str,
        provider_payload: Dict[str, Any],
        idempotency_key: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Unified purchase orchestration.

        Expected flow (high level):
        1. Validate provider receipt / token (validate_receipt_uc)
        2. Map provider transaction -> internal transaction model (transaction_mapper)
        3. Enforce idempotency (provider tx id + optional idempotency key)
        4. Persist Payment
        5. Fulfill product (fulfill_product_uc)
        6. Grant entitlements / wallet / subscription updates
        7. Return PurchaseResponse DTO

        Idempotency:
        - Same idempotency_key + same payload => return existing result
        - Same idempotency_key + different payload => conflict (409)
        - Same provider transaction id => return existing result
        """
        # 1. Validate the receipt / provider payload
        unified_transaction_result: Result = self.validate_receipt_uc.execute(
            receipt_data=provider_payload,
            provider=payment_provider,
        )

        if not isinstance(unified_transaction_result, Ok):
            return unified_transaction_result
        
        # ... enforce authenticated user owns this receipt
        unified_transaction: UnifiedTransactionDataVo = unified_transaction_result.value
        if unified_transaction.user_id and unified_transaction.user_id != user_id:
            return Result.NotOk(
                message="Receipt does not belong to authenticated user",
                static_msg="RECEIPT_USER_MISMATCH", # TODO: create static msg enum for payments
                status_code=403,
            )

        # 2. Fulfill purchase - prefer a single use-case that handles idempotency & persistence
        # fulfillment usecase returns none but Result still returned for possible errors. 
        fulfillment_result: Result = self.fulfill_product_uc.execute(
                    unified_transaction=unified_transaction,
                    user_id=user_id,
                    product_sku=product_sku,
                    quantity=quantity,
                    idempotency_key=idempotency_key,
                    metadata=metadata,
                )

        return fulfillment_result

    def purchase_coins(
        self,
        *,
        user_id: UUID,
        coin_type: str,
        num_of_coins: int,
        payment_provider: str,
        provider_payload: Dict[str, Any],
        idempotency_key: Optional[str] = None,
        client_reference: Optional[str] = None,
    ):
        """
        Convenience orchestration for consumable coin purchases.

        Expected flow:
        1. Validate receipt
        2. Enforce idempotency
        3. Persist Payment
        4. Deposit coins into wallet
        5. Return PurchaseResponse
        """
        raise NotImplementedError("Coordinate coin purchase validation, idempotency, wallet deposit")

    # ---------------------------------------------------------------------
    # Restore flows
    # ---------------------------------------------------------------------

    def restore_purchases(
        self,
        *,
        user_id: UUID,
        payment_provider: str,
        provider_payload: Dict[str, Any],
    ):
        """
        Restore non-consumable purchases and subscriptions.

        Expected flow:
        1. Validate provider payload
        2. Fetch historical transactions
        3. Re-sync subscriptions and entitlements
        4. Ignore consumables
        """
        raise NotImplementedError("Delegate to RestorePurchasesUseCase")

    # ---------------------------------------------------------------------
    # Stripe helpers
    # ---------------------------------------------------------------------

    def create_stripe_checkout_session(
        self,
        *,
        user_id: UUID,
        product_sku: str,
        success_url: str,
        cancel_url: str,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Create a Stripe Checkout Session.

        Notes:
        - No fulfillment here
        - Fulfillment happens via Stripe webhook
        """
        raise NotImplementedError("Delegate to payment gateway to create checkout session")

    # ---------------------------------------------------------------------
    # Read-only user views
    # ---------------------------------------------------------------------

    def get_user_entitlements(self, *, user_id: UUID):
        """
        Return all entitlements visible to a user.
        """
        raise NotImplementedError("Delegate to entitlement read service or repository")

    def get_user_subscriptions(self, *, user_id: UUID):
        """
        Return all subscriptions for a user.
        """
        raise NotImplementedError("Delegate to subscription read service or repository")

    # ---------------------------------------------------------------------
    # Product & payment lookup
    # ---------------------------------------------------------------------

    def get_product_variant(self, *, product_id: str):
        """
        Lookup product metadata by ID or internal SKU.
        """
        raise NotImplementedError("Delegate to product catalog repository")

    def get_payment(self, *, payment_id: UUID, requester_user_id: UUID):
        """
        Fetch a payment and enforce access control.
        """
        raise NotImplementedError("Lookup payment and enforce ownership / admin access")

    # ---------------------------------------------------------------------
    # Webhook entry points (idempotent by design)
    # ---------------------------------------------------------------------

    def handle_stripe_webhook(self, *, payload: Dict[str, Any], signature: str):
        """
        Handle Stripe webhook events.

        Expected:
        - Verify signature
        - Map event to internal transaction
        - Enforce idempotency
        - Fulfill or revoke as needed
        """
        raise NotImplementedError("Validate signature, parse event, route to webhook handler usecase")

    def handle_apple_webhook(self, *, payload: Dict[str, Any]):
        """
        Handle Apple App Store Server Notifications (JWS).
        """
        raise NotImplementedError("Validate JWS, parse notification, sync subscriptions")

    def handle_google_webhook(self, *, payload: Dict[str, Any]):
        """
        Handle Google Play RTDN webhook events.
        """
        raise NotImplementedError("Validate RTDN message, sync purchases")

    # ---------------------------------------------------------------------
    # Administrative / lifecycle actions
    # ---------------------------------------------------------------------

    def revoke_entitlement(
        self,
        *,
        user_id: UUID,
        entitlement_code: str,
        reason: Optional[str] = None,
    ):
        """
        Explicit entitlement revocation (refunds, abuse, admin actions).
        """
        raise NotImplementedError("Delegate to RevokeEntitlementUseCase")