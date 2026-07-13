from uuid import UUID
from datetime import datetime
from typing import Optional
from apps.authorization.domain.iusecases.icreate_object_acl_usecase import ICreateObjectACLUseCase
from apps.authorization.domain.entities.resource_identifier import ResourceIdentifierVo
from apps.authorization.domain.entities.object_acl_entry_entity import ObjectACLEntryEntity
from apps.authorization.domain.irepositories.iauthorization_repository import IAuthorizationRepository

class CreateObjectACLUseCase(ICreateObjectACLUseCase):
    def __init__(self, repository: IAuthorizationRepository):
        self.repository = repository

    def execute(
        self,
        resource: ResourceIdentifierVo,
        subject_type: str,
        subject_id: UUID,
        permission_codename: str,
        expires_at: Optional[datetime] = None,
    ) -> ObjectACLEntryEntity:
        # Logic: Create a specific rule for a specific resource
        return self.repository.create_acl_entry(
            resource_type=resource.resource_type,
            resource_id=resource.resource_id,
            subject_type=subject_type,
            subject_id=subject_id,
            permission_codename=permission_codename,
            expires_at=expires_at
        )