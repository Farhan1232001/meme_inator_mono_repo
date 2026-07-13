# domain/repositories/moderation_case_repository.py
from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional, List

from apps.moderation_sys.domain.aggregates.moderation_case import ModerationCase

class IModerationCaseRepository(ABC):
    @abstractmethod
    def save(self, case: ModerationCase) -> ModerationCase:
        pass

    @abstractmethod
    def find_by_id(self, case_id: UUID) -> Optional[ModerationCase]:
        pass

    @abstractmethod
    def find_pending_by_content_id(self, content_id: UUID) -> Optional[ModerationCase]:
        pass

    @abstractmethod
    def find_by_status(self, status: str, limit: int = 100) -> List[ModerationCase]:
        pass