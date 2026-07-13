# domain/irepositories/provider_health_repository.py
from abc import ABC, abstractmethod
from typing import Optional, List

from apps.moderation_sys.domain.aggregates.provider_health import ProviderHealth

class IProviderHealthRepository(ABC):
    @abstractmethod
    def save(self, health: ProviderHealth) -> ProviderHealth:
        """Save or update provider health state"""
        pass

    @abstractmethod
    def find_by_provider_name(self, provider_name: str) -> Optional[ProviderHealth]:
        """Find health state for a specific provider"""
        pass

    @abstractmethod
    def find_all(self) -> List[ProviderHealth]:
        """Find health states for all providers"""
        pass

    @abstractmethod
    def find_available_providers(self) -> List[ProviderHealth]:
        """Find all providers that are currently available (circuit closed or half-open)"""
        pass

    @abstractmethod
    def find_by_circuit_state(self, state: str) -> List[ProviderHealth]:
        """Find providers by circuit breaker state"""
        pass