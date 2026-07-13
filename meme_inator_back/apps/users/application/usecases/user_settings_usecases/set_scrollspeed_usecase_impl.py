from uuid import UUID
from apps.users.domain.usecases.user_settings_usecases.iset_scrollspeed_usecase import ISetScrollspeedUsecase
from apps.users.infrastructure.repositories.user_settings_repo import UserSettingsRepository

class SetScrollspeedUsecaseImpl(ISetScrollspeedUsecase):
    def __init__(self, settings_repo: UserSettingsRepository):
        self.settings_repo = settings_repo

    def execute(self, user_id: UUID, speed: float):
        self.settings_repo.update_settings(str(user_id), {"scroll_speed": speed})