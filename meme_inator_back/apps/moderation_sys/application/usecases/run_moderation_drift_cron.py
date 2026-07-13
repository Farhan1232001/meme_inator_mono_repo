# application/usecases/run_moderation_drift_cron.py
from uuid import UUID
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any
from apps.moderation_sys.domain.irepositories.drift_monitor_state_repository import IDriftMonitorStateRepository
from apps.moderation_sys.domain.irepositories.moderation_case_repository import IModerationCaseRepository
from apps.moderation_sys.domain.services.policy_registry_service import PolicyRegistryService
from core.results import Result, Ok, NotOk, Error

class RunModerationDriftCronJobUsecase:
    """Detect provider drift and alert - BP#7"""
    
    def __init__(
        self,
        drift_state_repo: IDriftMonitorStateRepository,
        case_repo: IModerationCaseRepository,
        policy_registry: PolicyRegistryService
    ):
        self.drift_state_repo = drift_state_repo
        self.case_repo = case_repo
        self.policy_registry = policy_registry

    def execute(self, lookback_hours: int = 24) -> Result:
        """Run drift detection cron job"""
        try:
            # Get recent moderation cases
            cutoff_time = datetime.now(timezone.utc) - timedelta(hours=lookback_hours)
            recent_cases = self.case_repo.find_recent_resolved(cutoff_time)
            
            drift_detected = []
            drift_observations = []
            
            for case in recent_cases:
                if not case.decision:
                    continue
                
                # Get policy for this case
                policy = self.policy_registry.lookup_active_policy(case.content.policy_routing_key)
                if not policy or not policy.drift_detection_policy:
                    continue
                
                # Create fingerprint for the case
                from domain.services.fingerprint_service import FingerprintDomainService
                fingerprint_hash = FingerprintDomainService.generate(case.content)
                
                # Find existing drift state
                drift_state = self.drift_state_repo.find_by_fingerprint(fingerprint_hash)
                
                if drift_state:
                    # Check for drift
                    confidence_delta = abs(case.confidence_score.value - drift_state.last_confidence)
                    previous_decision = drift_state.last_decision
                    current_decision = case.decision.outcome.value
                    provider_changed = drift_state.last_provider != case.provider_used
                    
                    drift_policy = policy.drift_detection_policy
                    
                    if drift_policy.is_drift(
                        previous_decision=previous_decision,
                        current_decision=current_decision,
                        confidence_delta=confidence_delta,
                        sample_count=drift_state.sample_count + 1
                    ):
                        drift_detected.append({
                            "fingerprint": fingerprint_hash,
                            "case_id": str(case.case_id),
                            "previous_provider": drift_state.last_provider.value,
                            "current_provider": case.provider_used.value,
                            "previous_decision": previous_decision,
                            "current_decision": current_decision,
                            "confidence_delta": confidence_delta
                        })
                        
                        # Emit alert (in real implementation)
                        self._emit_drift_alert(case, drift_state, confidence_delta)
                    
                    # Update drift state
                    drift_state.sample_count += 1
                    drift_state.last_confidence = case.confidence_score.value
                    drift_state.last_decision = current_decision
                    drift_state.last_provider = case.provider_used
                    drift_state.last_seen_at = datetime.now(timezone.utc)
                    
                    # Record observation for compliance
                    drift_observations.append({
                        "fingerprint": fingerprint_hash,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "provider": case.provider_used.value,
                        "decision": current_decision,
                        "confidence": case.confidence_score.value
                    })
                else:
                    # Create new drift state
                    from domain.aggregates.drift_monitor import DriftMonitorState
                    new_state = DriftMonitorState(
                        fingerprint=fingerprint_hash,
                        last_decision=case.decision.outcome.value,
                        last_confidence=case.confidence_score.value,
                        last_provider=case.provider_used,
                        last_seen_at=datetime.now(timezone.utc),
                        sample_count=1
                    )
                    drift_state = new_state
                
                self.drift_state_repo.save(drift_state)
            
            return Ok(value={
                "processed_cases": len(recent_cases),
                "drift_detected_count": len(drift_detected),
                "drift_detected": drift_detected,
                "observations_recorded": len(drift_observations)
            })
            
        except Exception as e:
            return Error(message="Failed to run drift detection", exception=e)
    
    def _emit_drift_alert(self, case, drift_state, confidence_delta):
        """Emit alert for drift detection"""
        # In real implementation, send to monitoring system
        alert = {
            "severity": "WARNING",
            "title": "Moderation Provider Drift Detected",
            "case_id": str(case.case_id),
            "fingerprint": drift_state.fingerprint,
            "confidence_delta": confidence_delta,
            "previous_provider": drift_state.last_provider.value,
            "current_provider": case.provider_used.value,
            "previous_decision": drift_state.last_decision,
            "current_decision": case.decision.outcome.value
        }
        print(f"DRIFT ALERT: {alert}")