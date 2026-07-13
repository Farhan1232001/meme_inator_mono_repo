from ninja_extra import NinjaExtraAPI, api_controller, http_get

from apps.app_system.application.dtos.app_sys_info_schema import AppSysInfoSchema
from apps.app_system.application.orchestration.app_sys_orchestration import AppSystemOrchestration
from apps.app_system.domain.entities.app_sys_info_entity import AppSystemInfoEntity
from apps.app_system.infrastructure.repositories.app_sys_repo_impl import AppSystemRepositoryImpl


@api_controller("/app_sys", tags=["app_sys"])
class AppSystemController:
    def __init__(self):
        self._orchestration = AppSystemOrchestration(
            AppSystemRepositoryImpl(cache=None, queue=None)
        )

    @http_get("/", response=AppSysInfoSchema)
    def get_system(self) -> AppSystemInfoEntity:
        return self._orchestration.get_app_sys_info()

    @http_get("/get_info", response=AppSysInfoSchema)
    def get_system_info(self) -> AppSystemInfoEntity:
        return self._orchestration.get_app_sys_info()

    