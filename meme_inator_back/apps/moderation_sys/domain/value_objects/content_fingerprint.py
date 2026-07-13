# domain/value_objects/content_fingerprint.py

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID
from apps.moderation_sys.domain.enums.moderation_enums import (
    ModerationProviderEnum, 
    DecisionEnum
)


@dataclass(frozen=True)
class ContentFingerprintVo:
    """
    Cryptographic fingerprint of content for deduplication and drift detection.
    
    The fingerprint_hash is the primary identifier (e.g., SHA-256).
    The 'value' field duplicates it for backward compatibility with comparison logic.
    """
    fingerprint_hash: str
    case_id: UUID
    content_type: str
    policy_routing_key: str
    provider_used: ModerationProviderEnum
    decision_outcome: DecisionEnum
    confidence_score: float
    created_at: datetime
    expires_at: datetime
    value: str  # This is the same as fingerprint_hash - kept for comparison methods

    def equals(self, other: 'ContentFingerprintVo') -> bool:
        """Compare two fingerprints for equality."""
        return self.fingerprint_hash == other.fingerprint_hash
    
    def is_expired(self) -> bool:
        """Check if the fingerprint has expired."""
        return datetime.now(timezone.utc) > self.expires_at