from enum import Enum


class ProductTypeEnum(str, Enum):
    SUBSCRIPTION = "SUBSCRIPTION"       # recurring (pro plan)
    CONSUMABLE = "CONSUMABLE"           # CC coins)
    NON_CONSUMABLE = "NON_CONSUMABLE"   # Lifetime unlock (No ads))