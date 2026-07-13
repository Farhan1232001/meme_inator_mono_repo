from abc import ABC, abstractmethod
from typing import Optional

from apps.authorization.domain.entities.permission_entity import PermissionEntity


class ICreatePermissionUseCase(ABC):
    @abstractmethod
    def execute(self, codename: str, description: Optional[str], role_name: Optional[str] = None) -> PermissionEntity:
        ...