from uuid import UUID
from apps.users.domain.usecases.user_settings_usecases.iget_static_urls_usecase import IGetStaticUrlsUsecase
from apps.users.infrastructure.repositories.user_settings_repo import UserSettingsRepository
from apps.app_system.domain.entities.static_urls_entity import StaticUrlsEntity

class GetStaticUrlsUsecaseImpl(IGetStaticUrlsUsecase):
    def __init__(self, settings_repo: UserSettingsRepository):
        self.settings_repo = settings_repo

    def execute(self, user_id: UUID) -> StaticUrlsEntity:
        settings = self.settings_repo.get_settings_by_user_id(str(user_id))
        if not settings:
            return StaticUrlsEntity(
                faq_url="",
                terms_of_service_url="",
                privacy_policy_url="",
                contact_support_url=""
            )
        return StaticUrlsEntity(
            faq_url=settings.faq_url or "",
            terms_of_service_url=settings.terms_of_service_url or "",
            privacy_policy_url=settings.privacy_policy_url or "",
            contact_support_url=settings.contact_support_url or ""
        )