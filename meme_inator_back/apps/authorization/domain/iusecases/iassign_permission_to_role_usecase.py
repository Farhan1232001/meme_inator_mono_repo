from abc import ABC, abstractmethod


class IAssignPermissionToRoleUseCase(ABC):
    @abstractmethod
    def execute(self, codename: str, role_name: str) -> None:
        ...