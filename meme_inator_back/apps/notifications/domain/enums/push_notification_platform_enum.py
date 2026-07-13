from enum import Enum

# Why have this?
# 1. Each platform uses different push notification services
# - web may use Web Push Protocol, IO uses Apple Push Notification Service (APNs), etc. 
# 2. Payload format differences

class PushPlatformEnum(str, Enum):
    WEB = "web"
    IOS = "ios"
    ANDROID = "android"
    OTHER = "other"