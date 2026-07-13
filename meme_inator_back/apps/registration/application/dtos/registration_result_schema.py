from typing import Dict, Optional
from ninja import Schema

from apps.profiles.application.dtos.profile_schema import ProfileSchema
from apps.users.application.dtos.user_schema import UserSchema

# TODO: Is this being used? Should Entities be outputs of usecases (user_register_usecase)?
class RegistrationResultSchema(Schema):
    user: UserSchema  # Replace with actual UserEntity schema
    profile: Optional[ProfileSchema] = None  # Replace with actual ProfileEntity schema
    requires_verification: bool = False
    tokens: Optional[Dict[str, str]] = None
