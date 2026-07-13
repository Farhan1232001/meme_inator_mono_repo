from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from apps.authorization.domain.entities.role_entity import RoleEntity


class IAssignRoleToUserUseCase(ABC):
    @abstractmethod
    def execute(self, actor_user_id: UUID, target_user_id: UUID, role_name: str) -> List[RoleEntity]:
        ...
