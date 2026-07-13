from django.db import models

from apps.feeds.domain.enums.feed_type import FeedType

class UserSettingsModel(models.Model):
    user = models.OneToOneField(
        "UserModel", on_delete=models.CASCADE, related_name="settings"
    )

    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)

    default_feed_type = models.CharField(
        max_length=32, choices=FeedType.choices, default=FeedType.FOR_YOU
    )

    is_appear_offline_on = models.BooleanField(default=False)
    theme_preference = models.CharField(max_length=64, blank=True, null=True)
    language_preference = models.CharField(max_length=16, blank=True, null=True)

    # granular notification toggles
    is_notification_on = models.BooleanField(default=True)
    is_new_messages_notification_on = models.BooleanField(default=True)
    is_replies_to_user_notification_on = models.BooleanField(default=True)
    is_comment_to_user_notification_on = models.BooleanField(default=True)
    is_sub_to_user_notification_on = models.BooleanField(default=True)

    # optional metadata/links
    app_icon = models.CharField(max_length=255, blank=True, null=True)
    faq_url = models.URLField(max_length=1024, blank=True, null=True)
    terms_of_service_url = models.URLField(max_length=1024, blank=True, null=True)
    privacy_policy_url = models.URLField(max_length=1024, blank=True, null=True)
    contact_support_url = models.URLField(max_length=1024, blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "user settings"
        verbose_name_plural = "user settings"
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["default_feed_type"]),
        ]

    def __str__(self):
        return f"Settings({self.user})"