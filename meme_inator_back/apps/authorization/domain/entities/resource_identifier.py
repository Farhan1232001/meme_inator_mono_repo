from dataclasses import dataclass
from uuid import UUID


@dataclass
class ResourceIdentifierVo:
    resource_type: str
    resource_id: UUID
