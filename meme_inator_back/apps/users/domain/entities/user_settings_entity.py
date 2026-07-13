from dataclasses import dataclass
from typing import Dict, Any

from apps.app_system.domain.entities.static_urls_entity import StaticUrlsEntity
from apps.users.domain.entities.preferences.accessibility_preferences_entity import AccessibilityPreferencesEntity
from apps.users.domain.entities.preferences.app_icon_preferences_entity import AppIconPreferencesEntity
from apps.users.domain.entities.preferences.display_preferences_entity import DisplayPreferencesEntity
from apps.users.domain.entities.preferences.feed_preferences_entity import FeedPreferencesEntity
from apps.users.domain.entities.preferences.language_preferences_entity import LanguagePreferencesEntity
from apps.users.domain.entities.preferences.notifications_preferences_entity import NotificationPreferencesEntity
from apps.users.domain.entities.preferences.privacy_preferences_entity import PrivacyPreferencesEntity
from apps.users.domain.entities.preferences.theme_preferences_entity import ThemePreferencesEntity


@dataclass
class UserSettingsEntity:
    accessibility_preferences: AccessibilityPreferencesEntity
    app_icon_preferences: AppIconPreferencesEntity
    display_preferences: DisplayPreferencesEntity
    feed_preferences: FeedPreferencesEntity
    language_preferences: LanguagePreferencesEntity
    notification_preferences: NotificationPreferencesEntity
    privacy_preferences: PrivacyPreferencesEntity
    static_urls: StaticUrlsEntity
    theme_preferences: ThemePreferencesEntity

    # --- Getters ---
    def get_accessibility_preferences(self) -> AccessibilityPreferencesEntity:
        return self.accessibility_preferences

    def get_app_icon_preferences(self) -> AppIconPreferencesEntity:
        return self.app_icon_preferences

    def get_display_preferences(self) -> DisplayPreferencesEntity:
        return self.display_preferences

    def get_feed_preferences(self) -> FeedPreferencesEntity:
        return self.feed_preferences

    def get_language_preferences(self) -> LanguagePreferencesEntity:
        return self.language_preferences

    def get_notification_preferences(self) -> NotificationPreferencesEntity:
        return self.notification_preferences

    def get_privacy_preferences(self) -> PrivacyPreferencesEntity:
        return self.privacy_preferences

    def get_static_urls(self) -> StaticUrlsEntity:
        return self.static_urls

    def get_theme_preferences(self) -> ThemePreferencesEntity:
        return self.theme_preferences

    # --- Behaviors ---
    def update(self, values: Dict[str, Any]) -> None:
        raise NotImplementedError
