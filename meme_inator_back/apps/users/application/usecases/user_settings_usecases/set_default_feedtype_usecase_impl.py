from uuid import UUID
from apps.users.domain.usecases.user_settings_usecases.iset_default_feedtype_usecase import ISetDefaultFeedtypeUsecase
from apps.users.infrastructure.repositories.user_settings_repo import UserSettingsRepository

class SetDefaultFeedtypeUsecaseImpl(ISetDefaultFeedtypeUsecase):
    def __init__(self, settings_repo: UserSettingsRepository):
        self.settings_repo = settings_repo

    def execute(self, user_id: UUID, feed_type: str):
        self.settings_repo.update_settings(str(user_id), {"default_feed_type": feed_type})