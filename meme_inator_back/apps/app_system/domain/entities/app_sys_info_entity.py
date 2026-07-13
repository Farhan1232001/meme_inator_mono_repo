# apps/app_system/domain/entities/app_system_info_entity.py
from pydantic.dataclasses import dataclass
from apps.app_system.infrastructure.models.app_sys_info_model import AppSystemInfoModel

@dataclass
class AppSystemInfoEntity:
    name: str
    version: str
    total_users: int
    total_posts: int
    active_online_users: int

    app_icon_url: str
    faq_page_url: str
    terms_of_service_url: str
    privacy_policy_url: str
    contact_support_url: str
