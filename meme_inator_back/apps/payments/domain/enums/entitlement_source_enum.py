from enum import Enum, auto

class EntitlementSourceEnum(str, Enum):
    """
    An enumeration to define the various sources from which a user entitlement
    could originate.
    """
    STRIPE = 'STRIPE'                       # Entitlement granted via the Stripe payment gateway
    APPLE_IAP = 'APPLE_IAP'                 # Entitlement granted via Apple In-App Purchase
    MANUAL_ADMIN_OVERRIDE = 'MANUAL_ADMIN_OVERRIDE'   # Entitlement manually applied by an administrator
    SYSTEM = 'SYSTEM'                       # Entitlement granted by the system automatically (e.g., a free trial, promotional offer)
    GOOGLE_PLAY = 'GOOGLE_PLAY'             # Entitlement granted via Google Play In-App Purchase
    PROMOTION = 'PROMOTION'                 # Entitlement granted as part of a specific marketing promotion
