from uuid import UUID
from apps.users.domain.usecases.user_settings_usecases.iset_feed_gridcolumbnum_usecase import ISetFeedGridColumbNumUsecase
from apps.users.infrastructure.repositories.user_settings_repo import UserSettingsRepository
from abc import ABC, abstractmethod

class SetFeedGridColumbNumUsecaseImpl(ISetFeedGridColumbNumUsecase):
    
    def __init__(self, settings_repo: UserSettingsRepository):
        self.settings_repo = settings_repo

    def execute(self, user_id: UUID, num: int):
        self.settings_repo.update_settings(str(user_id), {"feed_grid_column_number": num})