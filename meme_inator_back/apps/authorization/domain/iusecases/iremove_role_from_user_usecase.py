from abc import ABC, abstractmethod
from uuid import UUID


class IRemoveRoleFromUserUseCase(ABC):
    @abstractmethod
    def execute(self, actor_user_id: UUID, target_user_id: UUID, role_name: str) -> None:
        ...