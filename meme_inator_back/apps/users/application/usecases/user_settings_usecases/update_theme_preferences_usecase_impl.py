from uuid import UUID
from apps.users.domain.usecases.user_settings_usecases.iupdate_theme_preferences_usecase import IUpdateThemePreferencesUsecase
from apps.users.infrastructure.repositories.user_settings_repo import UserSettingsRepository

class UpdateThemePreferencesUsecaseImpl(IUpdateThemePreferencesUsecase):
    def __init__(self, settings_repo: UserSettingsRepository):
        self.settings_repo = settings_repo

    def execute(self, user_id: UUID, theme: str):
        self.settings_repo.update_settings(str(user_id), {"theme_preference": theme})