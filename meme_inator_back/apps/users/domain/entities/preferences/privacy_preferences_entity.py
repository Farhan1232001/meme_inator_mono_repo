
from dataclasses import dataclass


@dataclass
class PrivacyPreferencesEntity:
    is_appear_offline_on: bool

    def enable_appear_offline(self) -> None:
        self.is_appear_offline_on = True

    def disable_appear_offline(self) -> None:
        self.is_appear_offline_on = False
