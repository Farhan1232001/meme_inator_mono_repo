from dataclasses import dataclass


@dataclass
class LanguagePreferencesEntity:
    langauge_preferences: str # en, fr, etc

    def set_language(self, language: str):
        self.langauge_preferences = language