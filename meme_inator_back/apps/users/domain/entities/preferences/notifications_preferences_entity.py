from dataclasses import dataclass
from uuid import UUID

class UnknownNotificationPreferenceError(ValueError):
    """Is a ValueError"""
    pass

@dataclass
class NotificationPreferencesEntity:
    _user_id: UUID
    _is_notification_on: bool
    _is_new_messages_notification_on: bool
    _is_replies_to_user_notification_on: bool
    _is_comment_to_user_notification_on: bool
    _is_sub_to_user_notification_on: bool
    _is_email_notification_on: bool

    def enable_all(self) -> None:
        self._is_notification_on = True
        self._is_new_messages_notification_on = True
        self._is_replies_to_user_notification_on = True
        self._is_comment_to_user_notification_on = True
        self._is_sub_to_user_notification_on = True
        self._is_email_notification_on = True

    def disable_all(self) -> None:
        self._is_notification_on = False
        self._is_new_messages_notification_on = False
        self._is_replies_to_user_notification_on = False
        self._is_comment_to_user_notification_on = False
        self._is_sub_to_user_notification_on = False
        self._is_email_notification_on = False
        
    def set_notification(self, pref_name: str, enable: bool) -> None:
        """Sets the state of a specific notification preference using match."""
        match pref_name:
            case "notification_on":
                self._is_notification_on = enable
            case "new_messages_notification_on":
                self._is_new_messages_notification_on = enable
            case "replies_to_user_notification_on":
                self._is_replies_to_user_notification_on = enable
            case "comment_to_user_notification_on":
                self._is_comment_to_user_notification_on = enable
            case "sub_to_user_notification_on":
                self._is_sub_to_user_notification_on = enable
            case "email_notification_on":
                self._is_email_notification_on = enable
            case _:
                raise UnknownNotificationPreferenceError(
                    f"Unknown notification preference: '{pref_name}'"
                )

    def is_enabled(self, pref_name: str) -> None:
        """Checks if a specific notification preference is enabled using match."""
        match pref_name:
            case "notification_on":
                return self._is_notification_on
            case "new_messages_notification_on":
                return self._is_new_messages_notification_on
            case "replies_to_user_notification_on":
                return self._is_replies_to_user_notification_on
            case "comment_to_user_notification_on":
                return self._is_comment_to_user_notification_on
            case "sub_to_user_notification_on":
                return self._is_sub_to_user_notification_on
            case "email_notification_on":
                return self._is_email_notification_on
            case _:
                raise UnknownNotificationPreferenceError(
                    f"Unknown notification preference: '{pref_name}'"
                )

