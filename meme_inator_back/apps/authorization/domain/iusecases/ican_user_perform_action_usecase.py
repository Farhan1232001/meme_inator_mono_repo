from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from uuid import UUID

from apps.authorization.domain.entities.resource_identifier import ResourceIdentifierVo
from apps.authorization.domain.entities.value_objects.can_permission_response_vo import CanPermissionResponseVo


class ICanUserPerformActionUseCase(ABC):
    """
    Decide if a user may perform `action` on `resource` given `context`.
    """

    @abstractmethod
    def execute(
        self,
        user_id: UUID,
        action: str,
        resource: Optional[ResourceIdentifierVo] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> CanPermissionResponseVo:
        raise NotImplementedError