from uuid import UUID
from apps.users.domain.usecases.user_settings_usecases.iset_appicon_usecase import ISetAppIconUsecase
from apps.users.infrastructure.repositories.user_settings_repo import UserSettingsRepository

class SetAppIconUsecaseImpl(ISetAppIconUsecase):
    def __init__(self, settings_repo: UserSettingsRepository):
        self.settings_repo = settings_repo

    def execute(self, user_id: UUID, app_icon: str):
        self.settings_repo.update_settings(str(user_id), {"app_icon": app_icon})