from apps.app_system.domain.iusecases.i_get_app_sys_info_usecase import IGetAppSysInfoUsecase
from apps.app_system.domain.irepositories.i_app_sys_repository import IAppSystemRepository
from apps.app_system.domain.entities.app_sys_info_entity import AppSystemInfoEntity


class GetAppSysInfoUsecaseImpl(IGetAppSysInfoUsecase):
    """
    Implementation of the GetAppSysInfo usecase.
    Depends on the repository interface; infrastructure is injected.
    """

    def __init__(self, repository: IAppSystemRepository):
        self._repository = repository

    def execute(self) -> AppSystemInfoEntity:
        return self._repository.get_app_system_info()
