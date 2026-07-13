from abc import ABC, abstractmethod
from typing import Optional

from payments.domain.entities.product_variant_entity import ProductVariantEntity
from payments.domain.enums.payment_provider_enum import PaymentProviderEnum


class IProductVariantRepository(ABC):
    @abstractmethod
    def find_by_internal_sku(self, internal_sku: str) -> Optional[ProductVariantEntity]:
        raise NotImplementedError

    @abstractmethod
    def find_by_provider_product_id(
        self,
        provider: PaymentProviderEnum,
        provider_product_id: str,
    ) -> Optional[ProductVariantEntity]:
        """
        Used when resolving Apple / Google / Stripe product IDs
        back to internal SKU.
        """
        raise NotImplementedError
