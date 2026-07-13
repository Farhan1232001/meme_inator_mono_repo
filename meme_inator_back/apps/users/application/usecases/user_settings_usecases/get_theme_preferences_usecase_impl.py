from uuid import UUID
from apps.users.domain.usecases.user_settings_usecases.iget_theme_preferences_usecase import IGetThemePreferencesUsecase
from apps.users.infrastructure.repositories.user_settings_repo import UserSettingsRepository
from apps.users.domain.entities.preferences.theme_preferences_entity import ThemePreferencesEntity

class GetThemePreferencesUsecaseImpl(IGetThemePreferencesUsecase):
    def __init__(self, settings_repo: UserSettingsRepository):
        self.settings_repo = settings_repo

    def execute(self, user_id: UUID) -> ThemePreferencesEntity:
        settings = self.settings_repo.get_settings_by_user_id(str(user_id))
        if not settings:
            return ThemePreferencesEntity(theme_preferences="auto")
        return ThemePreferencesEntity(theme_preferences=settings.theme_preference or "auto")