from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class ObjectACLEntryEntity:
    acl_id: UUID
    resource_type: str
    resource_id: UUID
    subject_type: str  # 'user' or 'role'
    subject_id: UUID
    permission_codename: str
    granted_at: datetime
    expires_at: Optional[datetime]