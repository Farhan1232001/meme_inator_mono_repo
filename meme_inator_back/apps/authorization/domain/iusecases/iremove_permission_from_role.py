from abc import ABC, abstractmethod

class IRemovePermissionFromRoleUsecase(ABC):
    @abstractmethod
    def remove_permission_from_role(self, role_id: str, permission_id: str) -> None:
        """
        Remove a permission from a role.

        :param role_id: The ID of the role.
        :param permission_id: The ID of the permission to remove.
        """
        ...