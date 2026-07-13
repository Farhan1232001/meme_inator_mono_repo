
from dataclasses import dataclass
from uuid import UUID

from apps.users.domain.entities.preferences.accessibility_preferences_entity import AccessibilityPreferencesEntity
from apps.users.domain.entities.preferences.theme_preferences_entity import ThemePreferencesEntity





@dataclass
class DisplayPreferencesEntity:
    device_id: UUID
    theme_preferences: ThemePreferencesEntity
    accessibility_preferences: AccessibilityPreferencesEntity
    font_scale: float
    is_high_contrast_on: bool
    is_reduce_motion_on: bool
    preferred_video_quality: str   # e.g. auto, 144p, 240p, 360p, 480p, 720p, 1080p, 2160p
    is_data_saver_on: bool
    is_auto_play_on: bool

    # --- Getters / Setters ---
    def set_font_scale(self, scale: float) -> None:
        self.font_scale = scale

    def enable_high_contrast(self) -> None:
        self.is_high_contrast_on = True

    def disable_high_contrast(self) -> None:
        self.is_high_contrast_on = False

    def enable_reduce_motion(self) -> None:
        self.is_reduce_motion_on = True

    def disable_reduce_motion(self) -> None:
        self.is_reduce_motion_on = False

    def set_preferred_video_quality(self, quality: str) -> None:
        self.preferred_video_quality = quality

    def enable_data_saver(self) -> None:
        self.is_data_saver_on = True

    def disable_data_saver(self) -> None:
        self.is_data_saver_on = False

