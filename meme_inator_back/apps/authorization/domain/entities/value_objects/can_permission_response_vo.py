from dataclasses import dataclass
from uuid import UUID


@dataclass
class CanPermissionResponseVo:
    user_id: UUID
    action: str
    authorized: bool
