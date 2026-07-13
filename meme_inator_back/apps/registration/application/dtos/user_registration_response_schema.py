from typing import Optional, Dict
from ninja import Schema

class UserRegistrationResponseSchema(Schema):
    user: Optional[dict]
    profile: Optional[dict] = None
    requires_verification: bool
    tokens: Optional[dict] = None
