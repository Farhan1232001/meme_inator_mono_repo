from abc import ABC, abstractmethod
from uuid import UUID
from datetime import datetime
from apps.payments.domain.entities.subscription_entity import SubscriptionEntity
from apps.payments.domain.entities.unified_transaction_data_vo import UnifiedTransactionDataVo
from domain.enums import SubscriptionStatusEnum

class ISubscriptionService(ABC):
    """
    Interface for managing the lifecycle of subscriptions across all providers.
    """

    @abstractmethod
    def activate_or_update_subscription(
        self,
        user_id: UUID,
        transaction: UnifiedTransactionDataVo,
    ) -> SubscriptionEntity:
        """
        Creates or updates a subscription based on a successful payment or renewal.
        """
        ...

    @abstractmethod
    def extend_subscription(
        self,
        subscription: SubscriptionEntity,
        new_period_end: datetime,
    ) -> None:
        """
        Extends the current billing period (renewal).
        """
        ...

    @abstractmethod
    def cancel_at_period_end(
        self,
        subscription: SubscriptionEntity,
    ) -> None:
        """
        Marks subscription as canceling at the end of the current period.
        """
        ...

    @abstractmethod
    def expire_subscription(
        self,
        subscription: SubscriptionEntity,
    ) -> None:
        """
        Immediately expires a subscription (refund, revoke, provider cancel).
        """
        ...

    @abstractmethod
    def get_active_subscription(
        self,
        user_id: UUID,
        product_sku: str,
    ) -> SubscriptionEntity | None:
        """
        Fetches an active subscription if one exists.
        """
        ...