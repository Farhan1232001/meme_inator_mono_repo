from typing import Optional, Dict
from ninja import Schema

class UserRegistrationRequestSchema(Schema):
    username: str
    email: str
    raw_password: str
    accept_terms: bool = None
    locale: Optional[str] = None
