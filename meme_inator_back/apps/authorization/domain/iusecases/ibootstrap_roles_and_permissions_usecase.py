from abc import ABC, abstractmethod


class IBootstrapRolesAndPermissionsUseCase(ABC):
    @abstractmethod
    def execute(self) -> None:
        ...