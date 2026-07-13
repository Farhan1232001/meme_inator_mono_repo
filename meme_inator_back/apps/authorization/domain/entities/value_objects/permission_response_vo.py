from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class PermissionResponseVo:
    permission_id: UUID
    app_label: str
    codename: str
    description: Optional[str]
    created_at: datetime