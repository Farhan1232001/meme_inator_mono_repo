
from dataclasses import dataclass
from typing import Optional


@dataclass
class AppIconPreferencesEntity:
    app_icon_url: Optional[str]

    def set_app_icon(self, icon_name: str) -> None:
        self.app_icon_url = icon_name

    def reset_app_icon(self) -> None:
        raise NotImplementedError