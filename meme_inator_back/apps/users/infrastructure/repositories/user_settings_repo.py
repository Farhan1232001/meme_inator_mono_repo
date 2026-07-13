# apps/users/repositories/user_settings_repository.py
from typing import Optional, Dict, Any

from django.core.exceptions import ObjectDoesNotExist

from apps.users.infrastructure.models.user_settings_model import UserSettingsModel
from apps.users.infrastructure.models.user_model import UserModel
from apps.users.domain.entities.user_settings_entity import UserSettingsEntity


class UserSettingsRepository:
    """
    Handles data access for user settings and persistent state like online status.
    """

    def _map_to_settings_entity(self, settings_instance: UserSettingsModel) -> UserSettingsEntity:
        """
        Map a Django UserSettingsModel instance to a domain UserSettingsEntity.
        Includes the user's current is_online flag (stored on UserModel).
        """
        user = getattr(settings_instance, "user", None)
        is_online = getattr(user, "is_online", None) if user is not None else None

        return UserSettingsEntity(
            id=str(settings_instance.id),
            user_id=str(settings_instance.user_id) if getattr(settings_instance, "user_id", None) is not None else None,
            email_notifications=settings_instance.email_notifications,
            push_notifications=settings_instance.push_notifications,
            default_feed_type=settings_instance.default_feed_type,
            is_appear_offline_on=settings_instance.is_appear_offline_on,
            theme_preference=settings_instance.theme_preference,
            language_preference=settings_instance.language_preference,
            is_notification_on=settings_instance.is_notification_on,
            is_new_messages_notification_on=settings_instance.is_new_messages_notification_on,
            is_replies_to_user_notification_on=settings_instance.is_replies_to_user_notification_on,
            is_comment_to_user_notification_on=settings_instance.is_comment_to_user_notification_on,
            is_sub_to_user_notification_on=settings_instance.is_sub_to_user_notification_on,
            app_icon=settings_instance.app_icon,
            faq_url=settings_instance.faq_url,
            terms_of_service_url=settings_instance.terms_of_service_url,
            privacy_policy_url=settings_instance.privacy_policy_url,
            contact_support_url=settings_instance.contact_support_url,
            updated_at=settings_instance.updated_at,
            is_online=is_online,
        )

    def get_settings_by_user_id(self, user_id: str) -> Optional[UserSettingsEntity]:
        """
        Retrieve settings for a given user id. Returns None if not found.
        """
        try:
            settings_obj = UserSettingsModel.objects.select_related("user").get(user_id=user_id)
            return self._map_to_settings_entity(settings_obj)
        except ObjectDoesNotExist:
            return None

    def update_settings(self, user_id: str, data: Dict[str, Any]) -> Optional[UserSettingsEntity]:
        """
        Update or create the UserSettingsModel for the given user_id with `data` dict.
        Returns the mapped UserSettingsEntity, or None if the user doesn't exist.
        """
        try:
            user = UserModel.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return None

        # Only allow keys that exist on the model to avoid unexpected fields
        allowed_keys = {
            "email_notifications",
            "push_notifications",
            "default_feed_type",
            "is_appear_offline_on",
            "theme_preference",
            "language_preference",
            "is_notification_on",
            "is_new_messages_notification_on",
            "is_replies_to_user_notification_on",
            "is_comment_to_user_notification_on",
            "is_sub_to_user_notification_on",
            "app_icon",
            "faq_url",
            "terms_of_service_url",
            "privacy_policy_url",
            "contact_support_url",
        }
        filtered_defaults = {k: v for k, v in data.items() if k in allowed_keys}

        settings_obj, created = UserSettingsModel.objects.update_or_create(
            user=user,
            defaults=filtered_defaults,
        )
        return self._map_to_settings_entity(settings_obj)

    def set_visibility(self, user_id: str, is_online: bool) -> Optional[UserSettingsEntity]:
        """
        Sets the user's online visibility flag (on the UserModel) and returns the
        mapped UserSettingsEntity reflecting the new is_online state.

        If the user or settings record don't exist, the behavior:
         - If user doesn't exist -> returns None
         - If settings don't exist -> creates empty settings record and returns mapped entity
        """
        try:
            user = UserModel.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return None

        # Update the user's is_online flag (persistent state lives on the UserModel).
        user.is_online = bool(is_online)
        user.save(update_fields=["is_online"])

        # Ensure there's a settings object for this user to return a settings-entity
        settings_obj, _ = UserSettingsModel.objects.get_or_create(user=user)

        # Return settings entity which includes user.is_online in mapping
        return self._map_to_settings_entity(settings_obj)
