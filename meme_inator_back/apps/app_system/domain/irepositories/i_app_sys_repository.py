# apps/app_system/domain/irepositories/i_app_system_repository.py
from abc import ABC, abstractmethod
from apps.app_system.domain.entities.app_sys_info_entity import AppSystemInfoEntity

class IAppSystemRepository(ABC):
    """Repository interface for fetching App System information."""
    
    @abstractmethod
    def get_app_system_info(self) -> AppSystemInfoEntity:
        raise NotImplementedError
