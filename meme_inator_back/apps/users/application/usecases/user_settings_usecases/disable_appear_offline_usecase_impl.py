from uuid import UUID
from apps.users.domain.usecases.user_settings_usecases.idisable_appear_offline_usecase import IDisableAppearOfflineUsecase
from apps.users.infrastructure.repositories.user_settings_repo import UserSettingsRepository

class DisableAppearOfflineUsecaseImpl(IDisableAppearOfflineUsecase):
    def __init__(self, settings_repo: UserSettingsRepository):
        self.settings_repo = settings_repo

    def execute(self, user_id: UUID):
        self.settings_repo.update_settings(str(user_id), {"is_appear_offline_on": False})