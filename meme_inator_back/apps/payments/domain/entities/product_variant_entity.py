
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from apps.payments.domain.enums.product_type_enum import ProductTypeEnum


@dataclass
class ProductVariantEntity:
    """
    Product instance that can represent a product from a provider
    such as apple, google, or stripe
    """
    # 1. Internal Identity
    id: UUID
    internal_sku: str
    product_type: ProductTypeEnum

    # 2. Provider Mappings (external IDs)
    apple_product_id: Optional[str] = None
    google_product_id: Optional[str] = None
    stripe_price_id: Optional[str] = None

    # 3. Rewards & fulfillment related data
    entitlement_codename: Optional[str] = None
    token_grants_amount: Optional[int] = None

