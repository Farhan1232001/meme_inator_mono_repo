from dataclasses import dataclass
from typing import Dict, Optional

from apps.profiles.domain.entities.profile_entity import ProfileEntity
from apps.users.domain.entities.user_entity import UserEntity


@dataclass
class RegistrationResultEntity:
    user: UserEntity
    profile: Optional[ProfileEntity] = None
    requires_verification: bool = False
    tokens: Optional[Dict[str, str]] = None
