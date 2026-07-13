# apps/app_system/domain/models/app_system_info.py
from django.db import models

class AppSystemInfoModel(models.Model):
    """
    Django ORM model representing system-wide app information.
    Mirrors the AppSystemInfoEntity dataclass.
    """

    # Core information
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)

    total_users = models.PositiveIntegerField(default=0)
    total_posts = models.PositiveIntegerField(default=0)
    active_online_users = models.PositiveIntegerField(default=0)

    # Configuration URLs
    app_icon_url = models.URLField()
    faq_page_url = models.URLField()
    terms_of_service_url = models.URLField()
    privacy_policy_url = models.URLField()
    contact_support_url = models.URLField()

    class Meta:
        verbose_name = "App System Info"

    def __str__(self):
        return f"{self.name} (v{self.version})"
