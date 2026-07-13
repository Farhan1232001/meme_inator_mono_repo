from typing import Optional

from payments.domain.entities.product_variant_entity import ProductVariantEntity
from payments.domain.enums.payment_provider_enum import PaymentProviderEnum
from payments.domain.enums.product_type_enum import ProductTypeEnum
from payments.domain.irepositories.iproduct_variant_repository import IProductVariantRepository
from payments.infrastructure.models.product_variant_model import ProductVariantModel


class DjangoProductVariantRepository(IProductVariantRepository):

    def find_by_internal_sku(self, internal_sku: str) -> Optional[ProductVariantEntity]:
        model = ProductVariantModel.objects.filter(
            internal_sku=internal_sku
        ).first()

        return self._to_entity(model) if model else None

    def find_by_provider_product_id(
        self,
        provider: PaymentProviderEnum,
        provider_product_id: str,
    ) -> Optional[ProductVariantEntity]:

        lookup = {
            PaymentProviderEnum.APPLE_IAP: "apple_product_id",
            PaymentProviderEnum.GOOGLE_PLAY: "google_product_id",
            PaymentProviderEnum.STRIPE: "stripe_price_id",
        }[provider]

        model = ProductVariantModel.objects.filter(
            **{lookup: provider_product_id}
        ).first()

        return self._to_entity(model) if model else None

    def _to_entity(self, model: ProductVariantModel) -> ProductVariantEntity:
        return ProductVariantEntity(
            id=model.id,
            internal_sku=model.internal_sku,
            product_type=ProductTypeEnum(model.product_type),
            apple_product_id=model.apple_product_id,
            google_product_id=model.google_product_id,
            stripe_price_id=model.stripe_price_id,
            entitlement_codename=model.entitlement_codename,
            token_grants_amount=model.token_grants_amount,
        )
