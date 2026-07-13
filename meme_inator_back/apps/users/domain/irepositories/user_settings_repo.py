from abc import ABC, abstractmethod

from apps.users.domain.entities.user_settings_entity import UserSettingsEntity


class IUserSettingsRepository(ABC):
    """Contract for accessing and modifying user settings."""

    @abstractmethod
    def update_settings(self, user_id: str, data: Dict[str, Any]) -> UserSettingsEntity:
        pass

    @abstractmethod
    def set_visibility(self, user_id: str, is_online: bool) -> UserSettingsEntity:
        pass
