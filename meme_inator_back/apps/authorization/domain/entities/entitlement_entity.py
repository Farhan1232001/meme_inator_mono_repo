from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID


@dataclass
class EntitlementEntity:
    user_id: UUID
    code: str
    source: str
    granted_at: datetime
    expires_at: Optional[datetime]
    meta_data: Dict[str, Any]

    def is_active(self, now: Optional[datetime] = None) -> bool:
        raise NotImplementedError("EntitlementEntity.is_active not implemented")