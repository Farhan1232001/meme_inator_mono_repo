
from dataclasses import dataclass


@dataclass
class AccessibilityPreferencesEntity:
    is_subtitles_on: bool = False
    is_bold_text_on: bool = False
    is_thumb_nail_animation_on: bool = True

    def set_subtitles(self, on: bool):
        self.is_subtitles_on = on

    def set_bold_text(self, on: bool):
        self.is_bold_text_on = on

    def set_thumb_nail_animation(self, on: bool):
        self.is_thumb_nail_animation_on = on