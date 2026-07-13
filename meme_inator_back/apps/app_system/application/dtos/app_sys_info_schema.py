from pydantic import BaseModel

class AppSysInfoSchema(BaseModel):
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