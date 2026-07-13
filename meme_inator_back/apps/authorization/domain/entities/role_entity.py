from dataclasses import dataclass
import datetime
from typing import Optional
from uuid import UUID


@dataclass
class RoleEntity:
    role_id: UUID
    name: str
    description: Optional[str]
    is_default: bool
    created_at: datetime