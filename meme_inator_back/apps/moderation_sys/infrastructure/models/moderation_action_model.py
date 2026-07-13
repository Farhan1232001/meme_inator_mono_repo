from django.db import models

class ModerationActionChoices(models.TextChoices):
    PENDING_ACTION = "PENDING_ACTION",
    REJECT = "REJECT"
    ACCEPT = "ACCEPT"
    FLAG_FOR_HUMAN = "FLAG_FOR_HUMAN"
    FLAG = "FLAG"  # Mark for review, no visibility change yet
    QUARANTINE = "QUARANTINE"  # Only mods/admins can see; user sees their own (shadow state)
    TOMBSTONE = "TOMBSTONE"  # Replace with placeholder showing removal reason
    HIDE = "HIDE"  # Remove from public view; author can still see/edit
    DELETE = "DELETE"  # permanent removal; user cannot recover
    SHADOW_BAN = "SHADOW_BAN"
    SUSPEND = "SUSPEND"
    BAN = "BAN"
    PENDING_REVIEW = "PENDING_REVIEW"  # held in queue awaiting moderator
    HOLD = "HOLD"  # legal/compliance retension before action

class VisibilityEffectEnum(models.TextChoices):
    IMMEDIATE = "IMMEDIATE"
    DELAYED = "DELAYED"
    VISIBLE = "visible"
    HIDDEN = "hidden"

class ModerationActionModel(models.Model):
    action_type = models.CharField(
        max_length=50,
        choices=[(tag.value, tag.name) for tag in ModerationActionChoices]
    )
    visibility_effect = models.CharField(
        max_length=50,
        choices=[(tag.value, tag.name) for tag in VisibilityEffectEnum]
    )
    reason = models.TextField()

    class Meta:
        verbose_name = "Moderation Action"
        verbose_name_plural = "Moderation Actions"