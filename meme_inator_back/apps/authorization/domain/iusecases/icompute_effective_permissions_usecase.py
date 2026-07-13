from abc import ABC, abstractmethod
from typing import List
from uuid import UUID


class IComputeEffectivePermissionsUseCase(ABC):
    @abstractmethod
    def execute(self, user_id: UUID) -> List[str]:
        """
        Returns a precomputed list/set of permission slugs for caching.
        """
        ...
