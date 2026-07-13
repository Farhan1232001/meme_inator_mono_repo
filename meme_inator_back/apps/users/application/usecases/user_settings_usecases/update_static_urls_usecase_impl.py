from uuid import UUID
from apps.users.domain.usecases.user_settings_usecases.iupdate_static_urls_usecase import IUpdateStaticUrlsUsecase
from apps.users.infrastructure.repositories.user_settings_repo import UserSettingsRepository
from apps.app_system.domain.entities.static_urls_entity import StaticUrlsEntity

class UpdateStaticUrlsUsecaseImpl(IUpdateStaticUrlsUsecase):
    def __init__(self, settings_repo: UserSettingsRepository):
        self.settings_repo = settings_repo

    def execute(self, user_id: UUID, urls: StaticUrlsEntity):
        data = {
            "faq_url": urls.faq_url,
            "terms_of_service_url": urls.terms_of_service_url,
            "privacy_policy_url": urls.privacy_policy_url,
            "contact_support_url": urls.contact_support_url,
        }
        self.settings_repo.update_settings(str(user_id), data)