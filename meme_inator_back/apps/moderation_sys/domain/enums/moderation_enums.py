# domain/enums/moderation_enums.py
from enum import Enum

class CaseStatusEnum(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    RESOLVED = "RESOLVED"
    FLAGGED = "FLAGGED"
    APPEALING = "APPEALING"

class ModerationProviderEnum(str, Enum):
    OPENAI_API = "openai_moderation_api"
    PROVIDER_A = "PROVIDER_A"
    PROVIDER_B = "PROVIDER_B"
    FALLBACK = "FALLBACK"

class DecisionEnum(str, Enum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    FLAG = "FLAG"
    UNDECIDED = 'UNDECIDED'

class AppealStatusEnum(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DENIED = "DENIED"
    EXPIRED = "EXPIRED"

class AppealOutcomeEnum(str, Enum):
    APPROVED = "APPROVED"
    DENIED = "DENIED"

class CircuitBreakerStateEnum(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

class ModerationActionEnum(str, Enum):
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

    def is_visible_to_author(self) -> bool:
        return self not in (self.DELETE, self.SHADOW_BAN, self.SUSPEND, self.BAN)

    def is_visible_to_public(self) -> bool:
        return self in (self.ACCEPT, self.REJECT)

    def requires_review(self) -> bool:
        return self in (self.FLAG, self.FLAG_FOR_HUMAN, self.PENDING_REVIEW, self.HOLD)

class VisibilityEffectEnum(str, Enum):
    IMMEDIATE = "IMMEDIATE"
    DELAYED = "DELAYED"
    VISIBLE = "visible"
    HIDDEN = "hidden"

class ConfidenceBandEnum(str, Enum):
    HIGH = "HIGH"
    GREY = "GREY"
    LOW = "LOW"