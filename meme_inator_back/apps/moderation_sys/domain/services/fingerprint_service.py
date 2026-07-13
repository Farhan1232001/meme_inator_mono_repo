# domain/services/fingerprint_service.py

import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from apps.moderation_sys.domain.value_objects.content_to_mod.content_to_moderate import ContentToModerateVo
from apps.moderation_sys.domain.value_objects.content_fingerprint import ContentFingerprintVo
from apps.moderation_sys.domain.value_objects.content_snapshot_vo import ContentSnapshotVo
from apps.moderation_sys.domain.enums.moderation_enums import ModerationProviderEnum, DecisionEnum
from apps.moderation_sys.domain.services.content_fetcher.django_content_fetcher import DjangoContentFetcher
from core.results import NotOk


class FingerprintDomainService:
    """Service for generating and managing content fingerprints."""
    
    def __init__(self, content_fetcher: DjangoContentFetcher):
        self._content_fetcher = content_fetcher

    def generate(self, content_vo: ContentToModerateVo) -> str:
        """
        Generate a cryptographic hash of the actual content.
        Delegates all fetching to DjangoContentFetcher.
        """
        content_bytes:Optional[bytes] = self._content_fetcher.fetch_bytes(content_vo)
        if content_bytes:
            return hashlib.sha256(content_bytes).hexdigest()
        # Don't fallback to metadata_hash, must hash the image/video itself. 
        return None

    def _metadata_hash(self, content_vo: ContentToModerateVo) -> str:
        """Fallback when raw bytes not available."""
        data = f"{content_vo.content_type.value}:{content_vo.policy_routing_key}"
        
        if content_vo.text_content and content_vo.text_content.text:
            data += f":{content_vo.text_content.text[:100]}"
        if content_vo.image_content and content_vo.image_content.image_url:
            data += f":{content_vo.image_content.image_url}"
        if content_vo.video_content and content_vo.video_content.video_url:
            data += f":{content_vo.video_content.video_url}"
        
        return hashlib.sha256(data.encode()).hexdigest()

    @staticmethod
    def generate_from_snapshot(snapshot: ContentSnapshotVo) -> str:
        """Generate fingerprint hash from content snapshot metadata."""
        data = snapshot.fingerprint  # Already has the fingerprint
        if not data:
            # Fallback to text/URLs if fingerprint is not set
            parts = []
            if snapshot.text_snapshot and snapshot.text_snapshot.text:
                parts.append(snapshot.text_snapshot.text)
            if snapshot.image_snapshot and snapshot.image_snapshot.image_url:
                parts.append(snapshot.image_snapshot.image_url)
            if snapshot.video_snapshot and snapshot.video_snapshot.video_url:
                parts.append(snapshot.video_snapshot.video_url)
            data = ''.join(parts)
        return hashlib.sha256(data.encode()).hexdigest()

    def create_fingerprint_vo(
        self,
        content_vo: ContentToModerateVo,
        case_id: UUID,
        provider: ModerationProviderEnum,
        decision: DecisionEnum,
        confidence_score: float,
    ) -> ContentFingerprintVo:
        """Create a ContentFingerprintVo from content and metadata."""
        fingerprint_hash = self.generate(content_vo)
        
        return ContentFingerprintVo(
            fingerprint_hash=fingerprint_hash,
            case_id=case_id,
            content_type=content_vo.content_type.value,
            policy_routing_key=content_vo.policy_routing_key,
            provider_used=provider,
            decision_outcome=decision,
            confidence_score=confidence_score,
            created_at=datetime.now(timezone.utc),
            expires_at=datetime.now(timezone.utc) + timedelta(days=30),
            value=fingerprint_hash  # Keep value synced with fingerprint_hash
        )

    @staticmethod
    def compare_fingerprints(f1: ContentFingerprintVo, f2: ContentFingerprintVo) -> bool:
        """Compare two fingerprints for equality."""
        return f1.fingerprint_hash == f2.fingerprint_hash