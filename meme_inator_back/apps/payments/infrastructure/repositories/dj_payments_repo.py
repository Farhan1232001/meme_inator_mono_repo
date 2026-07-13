from typing import List, Optional
from uuid import UUID

from payments.domain.entities.payment_entity import PaymentEntity
from payments.domain.entities.money_vo import MoneyVo
from payments.domain.enums.payment_provider_enum import PaymentProviderEnum
from payments.domain.enums.payment_status_enum import PaymentStatusEnum
from payments.domain.irepositories.ipayment_repository import IPaymentRepository
from payments.infrastructure.models.payment_model import PaymentModel


class DjangoPaymentRepository(IPaymentRepository):

    def find_by_id(self, payment_id: UUID) -> Optional[PaymentEntity]:
        try:
            model = PaymentModel.objects.get(id=payment_id)
        except PaymentModel.DoesNotExist:
            return None

        return self._to_entity(model)

    def find_by_user_id(self, user_id: UUID) -> List[PaymentEntity]:
        """
        Fetches all payment history for a specific user.
        Needed for 'Restore Purchases' functionality.
        """
        # We order by created_at desc so we see newest attempts first (optional but good UX)
        models = PaymentModel.objects.filter(user_id=user_id).order_by('-created_at')
        return [self._to_entity(m) for m in models]

    def find_by_provider_transaction_id(
        self,
        provider: PaymentProviderEnum,
        provider_transaction_id: str,
    ) -> Optional[PaymentEntity]:
        try:
            model = PaymentModel.objects.get(
                provider=provider.value,
                provider_transaction_id=provider_transaction_id,
            )
        except PaymentModel.DoesNotExist:
            return None

        return self._to_entity(model)

    def save(self, payment: PaymentEntity) -> PaymentEntity:
        model = PaymentModel.objects.create(
            id=payment.id,
            user_id=payment.user_id,
            amt_cents=payment.money.amt_cents,
            currency=payment.money.currency,
            status=payment.status.value,
            provider=payment.provider.value,
            provider_transaction_id=payment.provider_transaction_id,
            provider_original_id=payment.provider_original_id,
            product_sku=payment.product_sku,
        )
        return self._to_entity(model)

    def update(self, payment: PaymentEntity) -> PaymentEntity:
        PaymentModel.objects.filter(id=payment.id).update(
            status=payment.status.value,
            amt_cents=payment.money.amt_cents,
            currency=payment.money.currency,
        )
        return self.find_by_id(payment.id)

    # -------------------------
    # Mapping helpers
    # -------------------------

    def _to_entity(self, model: PaymentModel) -> PaymentEntity:
        return PaymentEntity(
            id=model.id,
            user_id=model.user_id,
            money=MoneyVo(
                amt_cents=model.amt_cents,
                currency=model.currency,
            ),
            status=PaymentStatusEnum(model.status),
            provider=PaymentProviderEnum(model.provider),
            provider_transaction_id=model.provider_transaction_id,
            provider_original_id=model.provider_original_id,
            product_sku=model.product_sku,
            created_at=model.created_at,
        )
