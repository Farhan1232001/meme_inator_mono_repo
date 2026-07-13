from uuid import UUID, uuid7
from datetime import datetime
from apps.payments.domain.entities.product_variant_entity import ProductVariantEntity
from apps.payments.domain.entities.subscription_entity import SubscriptionEntity
from apps.payments.domain.entities.unified_transaction_data_vo import UnifiedTransactionDataVo
from apps.payments.domain.enums.subscription_status_enum import SubscriptionStatusEnum
from apps.payments.domain.irepositories.isubscription_repository import ISubscriptionRepository
from apps.payments.domain.iservices.isubscription_service import ISubscriptionService
import logging

logger = logging.getLogger(__name__)


class SubscriptionService(ISubscriptionService):
    """
    Manages lifecycle of subscriptions across all providers.
    """

    def __init__(self, subscription_repo: ISubscriptionRepository):
        self.subscription_repo = subscription_repo

    def fulfill_subscription(self, transaction: UnifiedTransactionDataVo, product: ProductVariantEntity) -> None:
        """
        TODO: create two different methods for activating subscription AND renewal of subscription
        Called by FulfillmentService. Links the transaction to a subscription.
        This Activates or Updates subscription
        """
        # 1. Try to find existing subscription by the Provider's ID 
        # (e.g., Stripe sub_ID or Apple original_transaction_id)
        sub = self.subscription_repo.find_by_provider_id(
            provider=transaction.provider,
            provider_subscription_id=transaction.original_transaction_id or transaction.provider_transaction_id
        )

        if sub:
            # Update existing (Renewal)
            sub.status = SubscriptionStatusEnum.ACTIVE
            sub.current_period_end = transaction.expires_date
            self.subscription_repo.update(sub)
        else:
            # Create new
            new_sub = SubscriptionEntity(
                id=uuid7(),
                user_id=transaction.user_id,
                status=SubscriptionStatusEnum.ACTIVE,
                product_sku=product.internal_sku,
                current_period_start=transaction.purchase_date,
                current_period_end=transaction.expires_date,
                cancel_at_period_end=False,
                provider=transaction.provider,
                provider_subscription_id=transaction.original_transaction_id or transaction.provider_transaction_id
            )
            self.subscription_repo.save(new_sub)

    def activate_or_update_subscription(
        self,
        user_id: UUID,
        transaction: UnifiedTransactionDataVo,
        product_sku: str,
    ) -> SubscriptionEntity:
        """
        Business logic for resolving whether this is a new sub or a renewal.
        """
        # We look up by the 'Parent' ID (original_transaction_id) to link renewals
        provider_sub_id = transaction.original_transaction_id or transaction.provider_transaction_id
        
        subscription = self.subscription_repo.find_by_provider_subscription_id(
            provider=transaction.provider,
            provider_subscription_id=provider_sub_id
        )

        if subscription:
            # RENEWAL LOGIC
            logger.info(f"Renewing subscription {provider_sub_id} for user {user_id}")
            self.extend_subscription(subscription, transaction.expires_date)
            return subscription
        
        # NEW SUBSCRIPTION LOGIC
        logger.info(f"Creating new subscription for user {user_id}")
        new_sub = SubscriptionEntity(
            id=uuid7(),
            user_id=user_id,
            status=SubscriptionStatusEnum.ACTIVE,
            product_sku=product_sku,
            current_period_start=transaction.purchase_date,
            current_period_end=transaction.expires_date,
            cancel_at_period_end=False,
            provider=transaction.provider,
            provider_subscription_id=provider_sub_id
        )
        return self.subscription_repo.save(new_sub)

    def extend_subscription(
        self,
        subscription: SubscriptionEntity,
        new_period_end: datetime,
    ) -> None:
        """
        Updates the end date and ensures status is ACTIVE (handles re-activations).
        """
        subscription.extend_period(new_period_end)
        subscription.status = SubscriptionStatusEnum.ACTIVE
        # If they previously canceled but then renewed, we reset the cancel flag
        subscription.set_cancel_at_end(False) 
        
        self.subscription_repo.update(subscription)

    def cancel_at_period_end(
        self,
        subscription: SubscriptionEntity,
    ) -> None:
        """
        User clicked 'Cancel' but still has access until the current period expires.
        """
        subscription.set_cancel_at_end(True)
        self.subscription_repo.update(subscription)

    def expire_subscription(
        self,
        subscription: SubscriptionEntity,
    ) -> None:
        """
        Hard expiration: Used for refunds, chargebacks, or when the grace period ends.
        """
        subscription.expire()
        self.subscription_repo.update(subscription)

    def get_active_subscription(
        self,
        user_id: UUID,
        product_sku: str,
    ) -> SubscriptionEntity | None:
        """
        Checks repository for a valid subscription and double-verifies the clock.
        """
        sub = self.subscription_repo.find_active_by_user_and_sku(user_id, product_sku)
        
        # Safety check: Even if DB says ACTIVE, check the current time
        if sub and sub.is_expired():
            # Trigger background expiration if we caught an expired one
            self.expire_subscription(sub)
            return None
            
        return sub