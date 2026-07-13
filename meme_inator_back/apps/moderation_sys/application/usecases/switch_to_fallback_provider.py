# application/usecases/switch_to_fallback_provider.py
from uuid import UUID
from datetime import datetime, timezone, timedelta
from apps.moderation_sys.domain.enums.moderation_enums import ModerationProviderEnum
from apps.moderation_sys.domain.irepositories.provider_health_repository import IProviderHealthRepository
from core.results import Result, Ok, NotOk, Error

class SwitchToFallbackProviderUsecase:
    """Switch to fallback provider when primary is down - BP#8"""
    
    def __init__(self, provider_health_repo: IProviderHealthRepository):
        self.provider_health_repo = provider_health_repo

    def execute(self, primary_provider: str) -> Result:
        """Check provider health and switch if needed"""
        try:
            provider_enum = ModerationProviderEnum(primary_provider)
            health = self.provider_health_repo.find_by_provider(provider_enum)
            
            if not health:
                return NotOk(message="Provider health not found", static_msg="PROVIDER_NOT_FOUND")
            
            # Check if provider is available
            if not health.is_available():
                # Determine fallback provider
                fallback_provider = self._determine_fallback(provider_enum)
                
                # Check if fallback is healthy
                fallback_health = self.provider_health_repo.find_by_provider(fallback_provider)
                if fallback_health and fallback_health.is_available():
                    return Ok(value={
                        "switch_to": fallback_provider.value,
                        "primary_provider": provider_enum.value,
                        "primary_status": health.circuit_breaker_state,
                        "switch_time": datetime.now(timezone.utc).isoformat()
                    })
                else:
                    # Try to reset circuit breaker for testing
                    if health.circuit_breaker_state == "OPEN":
                        # Check if enough time has passed to try half-open
                        time_since_change = datetime.now(timezone.utc) - health.last_state_change
                        if time_since_change > timedelta(minutes=5):
                            health.attempt_reset()
                            self.provider_health_repo.save(health)
                            return Ok(value={
                                "status": "ATTEMPTING_RESET",
                                "provider": provider_enum.value,
                                "message": "Circuit breaker moved to HALF_OPEN"
                            })
                    
                    return NotOk(
                        message="No healthy provider available", 
                        static_msg="NO_HEALTHY_PROVIDER"
                    )
            
            return Ok(value={
                "status": "HEALTHY",
                "provider": provider_enum.value,
                "circuit_breaker_state": health.circuit_breaker_state
            })
            
        except Exception as e:
            return Error(message="Failed to check provider health", exception=e)
    
    def _determine_fallback(self, primary: ModerationProviderEnum) -> ModerationProviderEnum:
        """Determine fallback provider based on primary"""
        if primary == ModerationProviderEnum.PROVIDER_A:
            return ModerationProviderEnum.PROVIDER_B
        elif primary == ModerationProviderEnum.PROVIDER_B:
            return ModerationProviderEnum.PROVIDER_A
        else:
            return ModerationProviderEnum.FALLBACK