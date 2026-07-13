# infrastructure/repositories/django_drift_monitor_state_repository.py
from typing import Optional, List
from datetime import datetime, timedelta, timezone

from apps.moderation_sys.domain.irepositories.drift_monitor_state_repository import IDriftMonitorStateRepository
from apps.moderation_sys.infrastructure.models.drift_monitor_state_model import DriftMonitorStateModel



class DjangoDriftMonitorStateRepository(IDriftMonitorStateRepository):
    
    def save(self, state: DriftMonitorState) -> DriftMonitorState:
        """Save or update drift monitor state"""
        model, created = DriftMonitorStateModel.objects.update_or_create(
            fingerprint_hash=state.fingerprint_hash,
            defaults={
                'case_id': state.case_id,
                'last_decision': state.last_decision,
                'last_provider': state.last_provider,
                'last_confidence': state.last_confidence,
                'last_seen_at': state.last_seen_at,
                'drift_detected': state.drift_detected,
                'drift_detected_at': state.drift_detected_at,
                'previous_provider': state.previous_provider,
                'previous_decision': state.previous_decision,
                'confidence_delta': state.confidence_delta,
            }
        )
        return self._to_domain(model)
    
    def find_by_fingerprint(self, fingerprint: str) -> Optional[DriftMonitorState]:
        """Find drift monitor state by content fingerprint"""
        try:
            model = DriftMonitorStateModel.objects.get(fingerprint_hash=fingerprint)
            return self._to_domain(model)
        except DriftMonitorStateModel.DoesNotExist:
            return None
    
    def find_all_active(self, limit: int = 1000) -> List[DriftMonitorState]:
        """Find all active drift monitor states"""
        models = DriftMonitorStateModel.objects.all().order_by('-last_seen_at')[:limit]
        return [self._to_domain(model) for model in models]
    
    def find_by_provider(self, provider_name: str) -> List[DriftMonitorState]:
        """Find drift states for a specific provider"""
        models = DriftMonitorStateModel.objects.filter(
            last_provider=provider_name
        ).order_by('-last_seen_at')
        
        return [self._to_domain(model) for model in models]
    
    def find_stale_states(self, older_than_days: int = 30) -> List[DriftMonitorState]:
        """Find states that haven't been updated recently"""
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=older_than_days)
        models = DriftMonitorStateModel.objects.filter(
            last_seen_at__lt=cutoff_date
        )
        
        return [self._to_domain(model) for model in models]
    
    def delete_by_fingerprint(self, fingerprint: str) -> bool:
        """Delete a drift monitor state by fingerprint"""
        try:
            model = DriftMonitorStateModel.objects.get(fingerprint_hash=fingerprint)
            model.delete()
            return True
        except DriftMonitorStateModel.DoesNotExist:
            return False
    
    def _to_domain(self, model: DriftMonitorStateModel) -> DriftMonitorState:
        """Convert model to domain aggregate"""
        return DriftMonitorState(
            fingerprint_hash=model.fingerprint_hash,
            case_id=model.case_id,
            last_decision=model.last_decision,
            last_provider=model.last_provider,
            last_confidence=model.last_confidence,
            last_seen_at=model.last_seen_at,
            created_at=model.created_at,
            drift_detected=model.drift_detected,
            drift_detected_at=model.drift_detected_at,
            previous_provider=model.previous_provider,
            previous_decision=model.previous_decision,
            confidence_delta=model.confidence_delta
        )