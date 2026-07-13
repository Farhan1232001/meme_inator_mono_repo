from apps.app_system.domain.entities.app_sys_info_entity import AppSystemInfoEntity
from apps.app_system.domain.irepositories.i_app_sys_repository import IAppSystemRepository
from apps.app_system.application.usecases.get_app_sys_info_usecase import GetAppSysInfoUsecaseImpl

class AppSystemOrchestration:
    def __init__(self, app_sys_repo: IAppSystemRepository):
        self._get_info_usecase = GetAppSysInfoUsecaseImpl(
            repository=app_sys_repo 
        )

    def get_app_sys_info(self) -> AppSystemInfoEntity:
        return self._get_info_usecase.execute()
