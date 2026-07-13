from enum import Enum


class PaymentProviderEnum(str, Enum):
    STRIPE = "STRIPE"
    APPLE_IAP = "APPLE_IAP"
    GOOGLE_PLAY = "GOOGLE_PLAY"