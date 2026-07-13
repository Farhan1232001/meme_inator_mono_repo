from typing import Optional
from uuid import UUID

from payments.domain.entities.subscription_entity import SubscriptionEntity
from payments.domain.enums.payment_provider_enum import PaymentProviderEnum
from payments.domain.enums.subscription_status_enum import SubscriptionStatusEnum
from payments.domain.irepositories.isubscription_repository import ISubscriptionRepository
from payments.infrastructure.models.subscription_model import SubscriptionModel


class DjangoSubscriptionRepository(ISubscriptionRepository):

    def find_by_id(self, subscription_id: UUID) -> Optional[SubscriptionEntity]:
        try:
            model = SubscriptionModel.objects.get(id=subscription_id)
        except SubscriptionModel.DoesNotExist:
            return None

        return self._to_entity(model)

    def find_by_provider_subscription_id(
        self,
        provider: PaymentProviderEnum,
        provider_subscription_id: str,
    ) -> Optional[SubscriptionEntity]:
        try:
            model = SubscriptionModel.objects.get(
                provider=provider.value,
                provider_subscription_id=provider_subscription_id,
            )
        except SubscriptionModel.DoesNotExist:
            return None

        return self._to_entity(model)

    def find_active_by_user_and_sku(
        self,
        user_id: UUID,
        product_sku: str,
    ) -> Optional[SubscriptionEntity]:
        model = (
            SubscriptionModel.objects
            .filter(user_id=user_id, product_sku=product_sku)
            .exclude(status=SubscriptionStatusEnum.EXPIRED.value)
            .first()
        )

        return self._to_entity(model) if model else None

    def save(self, subscription: SubscriptionEntity) -> SubscriptionEntity:
        model = SubscriptionModel.objects.create(
            id=subscription.id,
            user_id=subscription.user_id,
            status=subscription.status.value,
            product_sku=subscription.product_sku,
            current_period_start=subscription.current_period_start,
            current_period_end=subscription.current_period_end,
            cancel_at_period_end=subscription.cancel_at_period_end,
            provider=subscription.provider.value,
            provider_subscription_id=subscription.provider_subscription_id,
        )
        return self._to_entity(model)

    def update(self, subscription: SubscriptionEntity) -> SubscriptionEntity:
        SubscriptionModel.objects.filter(id=subscription.id).update(
            status=subscription.status.value,
            current_period_start=subscription.current_period_start,
            current_period_end=subscription.current_period_end,
            cancel_at_period_end=subscription.cancel_at_period_end,
        )
        return self.find_by_id(subscription.id)

    def _to_entity(self, model: SubscriptionModel) -> SubscriptionEntity:
        return SubscriptionEntity(
            id=model.id,
            user_id=model.user_id,
            status=SubscriptionStatusEnum(model.status),
            product_sku=model.product_sku,
            current_period_start=model.current_period_start,
            current_period_end=model.current_period_end,
            cancel_at_period_end=model.cancel_at_period_end,
            provider=PaymentProviderEnum(model.provider),
            provider_subscription_id=model.provider_subscription_id,
        )
