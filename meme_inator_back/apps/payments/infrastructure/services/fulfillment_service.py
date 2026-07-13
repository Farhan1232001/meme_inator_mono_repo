# application/services/fulfilment_service.py
from uuid import UUID, uuid7
from apps.payments.domain.entities.money_vo import MoneyVo
from apps.payments.domain.entities.payment_entity import PaymentEntity
from apps.payments.domain.entities.product_variant_entity import ProductVariantEntity
from apps.payments.domain.iservices.ientitlement_service import IEntitlementService
from apps.payments.domain.iservices.isubscription_service import ISubscriptionService
from apps.payments.domain.iservices.iwallet_service import IWalletService
from domain.entities.unified_transaction_data_vo import UnifiedTransactionDataVo
from domain.enums.product_type_enum import ProductTypeEnum
from domain.irepositories.iproduct_variant_repository import IProductVariantRepository
from domain.irepositories.ipayment_repository import IPaymentRepository
from domain.irepositories.isubscription_repository import ISubscriptionRepository
from domain.irepositories.ientitlement_repository import IEntitlementRepository
from domain.iservices.ifulfilment_service import IFulfillmentService
import logging
from django.db import transaction as db_transaction

logger = logging.getLogger(__name__)

class FulfillmentService(IFulfillmentService):
    """
    Application-level coordinator that fulfills a purchase.
    It keeps the "what" (routing) separate from the "how" the domain logic

    Responsibilities:
    - Resolve ProductVariant from SKU
    - Perform idempotency-safe fulfillment
    - Route to Wallet / Subscription / Entitlement logic
    """

    def __init__(
        self,
        product_repo: IProductVariantRepository,
        payment_repo: IPaymentRepository,
        wallet_service: IWalletService,
        subscription_service: ISubscriptionService,
        entitlement_service: IEntitlementService,
    ):
        self.product_repo = product_repo
        self.payment_repo = payment_repo
        self.wallet_service = wallet_service
        self.subscription_service = subscription_service
        self.entitlement_service = entitlement_service

    def fulfill_purchase(self, transaction_vo: UnifiedTransactionDataVo) -> None:
        """
        Entry point called ONLY after payment success is confirmed.
        Flow:
            1. Resolve ProductVariant via SKU
                Resolve means take "dirty" external info 
                and map it to a "clean" internal/verifed object 
                this system understands. Basically its a translator to an instance
                this system understands. 
            2. Idempotency check via PaymentRepository
            3. Branch by ProductType
        """
        # 1. Resolve ProductVariant via Provider's Product ID
        product = self.product_repo.find_by_provider_product_id(
            provider=transaction_vo.provider,
            provider_product_id=transaction_vo.product_id
        )

        if not product:
            logger.error(f"Fulfillment failed: No internal SKU found for {transaction_vo.provider} product {transaction_vo.product_id}")
            raise ValueError("Unrecognized product variant.")

        # 2. Idempotency check: Ensure we haven't processed this transaction ID before
        with db_transaction.atomic():
            #...Intempotency check
            existing_payment = self.payment_repo.find_by_provider_transaction_id(
                provider=transaction_vo.provider,
                provider_transaction_id=transaction_vo.provider_transaction_id
            )
            
            if existing_payment:
                logger.info(f"Transaction {transaction_vo.get_unique_lookup_key()} already fulfilled. Skipping.")
                return

            # 3. Create and PERSIST the Payment record
            payment_record = PaymentEntity(
                id=uuid7(),
                user_id=transaction_vo.user_id,
                money=MoneyVo(
                    amt_cents=int(transaction_vo.amount_decimal * 100), # Standardizing to cents
                    currency=transaction_vo.currency
                ),
                status=transaction_vo.status,
                provider=transaction_vo.provider,
                provider_transaction_id=transaction_vo.provider_transaction_id,
                provider_original_id=transaction_vo.original_transaction_id,
                product_sku=product.internal_sku
            )
            self.payment_repo.save(payment_record)

            # 4. Branch by ProductType to fulfill the actual "benefit"
            self._fulfill_product_benefits(transaction_vo, product)
        
        logger.info(f"Successfully fulfilled {product.product_type} for user {transaction_vo.user_id}")


    def attempt_restoration(self, payment: PaymentEntity) -> bool:
        """
        Handles HISTORICAL receipts from local DB.
        """
        product = self.product_repo.find_by_sku(payment.product_sku)
        if not product:
            return False

        # RULE: We DO NOT restore Subscriptions from local Payment History.
        # Why? Because a payment record from 2022 doesn't tell us if the 
        # subscription is active TODAY. Subscription restoration should happen 
        # via 'Sync with Provider' or Webhooks, not local DB loops.
        if product.product_type == ProductTypeEnum.SUBSCRIPTION:
            logger.debug(f"Skipping local restoration for Subscription {payment.id}")
            return False

        if product.product_type == ProductTypeEnum.CONSUMABLE:
            return False

        self._fulfill_product_benefits(payment, product)
        return True


    def _fulfill_product_benefits(self, transaction_vo: UnifiedTransactionDataVo, product: ProductVariantEntity) -> None:
        """
        Routes the transaction to the specific service based on product type.
        benefit (legally) == advantage, profit, or gain (financial or non-financial) 
            received from a contract, action, or property

        Note: We only pass user_id and product to keep it compatible with 
        both new purchases and restorations.
        """
        if product.product_type == ProductTypeEnum.SUBSCRIPTION:
            # Note: You may need to pass the transaction_vo/payment if 
            # subscription_service needs specific dates.
            self.subscription_service.fulfill_subscription(transaction_vo.user_id, product)

        elif product.product_type == ProductTypeEnum.CONSUMABLE:
            if product.token_grants_amount:
                self.wallet_service.grant_tokens(
                    user_id=transaction_vo.user_id, 
                    amount=product.token_grants_amount
                )

        elif product.product_type == ProductTypeEnum.NON_CONSUMABLE:
            if product.entitlement_codename:
                self.entitlement_service.grant_entitlement(
                    user_id=transaction_vo.user_id,
                    codename=product.entitlement_codename,
                    source="FULFILLMENT_SERVICE"
                )
