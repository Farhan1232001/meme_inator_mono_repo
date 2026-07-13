
from dataclasses import dataclass


@dataclass
class ThemePreferencesEntity:
    theme_preferences: str # light, dark, auto

    def set_theme(self, theme: str) -> None:
        raise NotImplementedError