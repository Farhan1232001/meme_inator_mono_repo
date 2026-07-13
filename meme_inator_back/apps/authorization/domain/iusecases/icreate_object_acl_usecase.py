from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from uuid import UUID

from apps.authorization.domain.entities.object_acl_entry_entity import ObjectACLEntryEntity
from apps.authorization.domain.entities.resource_identifier import ResourceIdentifierVo


class ICreateObjectACLUseCase(ABC):
    @abstractmethod
    def execute(
        self,
        resource: ResourceIdentifierVo,
        subject_type: str,
        subject_id: UUID,
        permission_codename: str,
        expires_at: Optional[datetime] = None,
    ) -> ObjectACLEntryEntity:
        ...