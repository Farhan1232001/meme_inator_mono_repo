from uuid import UUID
from apps.users.domain.usecases.user_settings_usecases.iget_language_preferences_usecase import IGetLanguagePreferencesUsecase
from apps.users.infrastructure.repositories.user_settings_repo import UserSettingsRepository
from apps.users.domain.entities.preferences.language_preferences_entity import LanguagePreferencesEntity

class GetLanguagePreferencesUsecaseImpl(IGetLanguagePreferencesUsecase):
    def __init__(self, settings_repo: UserSettingsRepository):
        self.settings_repo = settings_repo

    def execute(self, user_id: UUID) -> LanguagePreferencesEntity:
        settings = self.settings_repo.get_settings_by_user_id(str(user_id))
        if not settings:
            return LanguagePreferencesEntity(langauge_preferences="en")
        return LanguagePreferencesEntity(langauge_preferences=settings.language_preference or "en")