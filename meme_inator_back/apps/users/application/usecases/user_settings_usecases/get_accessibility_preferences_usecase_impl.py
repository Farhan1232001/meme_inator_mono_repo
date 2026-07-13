from uuid import UUID
from apps.users.domain.usecases.user_settings_usecases.iget_accessibility_preferences_usecase import IGetAccessibilityPreferencesUsecase
from apps.users.infrastructure.repositories.user_settings_repo import UserSettingsRepository
from apps.users.domain.entities.preferences.accessibility_preferences_entity import AccessibilityPreferencesEntity

class GetAccessibilityPreferencesUsecaseImpl(IGetAccessibilityPreferencesUsecase):
    def __init__(self, settings_repo: UserSettingsRepository):
        self.settings_repo = settings_repo

    def execute(self, user_id: UUID) -> AccessibilityPreferencesEntity:
        # Return default if not stored; you can extend this later
        return AccessibilityPreferencesEntity()