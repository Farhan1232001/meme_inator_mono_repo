# apps/app_system/domain/usecases/i_get_app_sys_info_usecase.py
from abc import ABC, abstractmethod
from apps.app_system.domain.entities.app_sys_info_entity import AppSystemInfoEntity

class IGetAppSysInfoUsecase(ABC):
    @abstractmethod
    def execute(self) -> AppSystemInfoEntity:
        raise NotImplementedError
