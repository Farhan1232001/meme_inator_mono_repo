from uuid import UUID
from apps.users.domain.usecases.user_settings_usecases.iset_boldtext_usecase import ISetBoldtextUsecase
from apps.users.infrastructure.repositories.user_settings_repo import UserSettingsRepository

class SetBoldtextUsecaseImpl(ISetBoldtextUsecase):
    def __init__(self, settings_repo: UserSettingsRepository):
        self.settings_repo = settings_repo

    def execute(self, user_id: UUID, enabled: bool):
        self.settings_repo.update_settings(str(user_id), {"bold_text": enabled})