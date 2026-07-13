# domain/irepositories/drift_monitor_state_repository.py
from abc import ABC, abstractmethod
from typing import Optional, List

class IDriftMonitorStateRepository(ABC):
    @abstractmethod
    def save(self, state: DriftMonitorState) -> DriftMonitorState:
        """Save or update drift monitor state"""
        pass

    @abstractmethod
    def find_by_fingerprint(self, fingerprint: str) -> Optional[DriftMonitorStateEntity]:
        """Find drift monitor state by content fingerprint"""
        pass

    @abstractmethod
    def find_all_active(self, limit: int = 1000) -> List[DriftMonitorState]:
        """Find all active drift monitor states"""
        pass

    @abstractmethod
    def find_by_provider(self, provider_name: str) -> List[DriftMonitorState]:
        """Find drift states for a specific provider"""
        pass

    @abstractmethod
    def find_stale_states(self, older_than_days: int = 30) -> List[DriftMonitorState]:
        """Find states that haven't been updated recently"""
        pass

    @abstractmethod
    def delete_by_fingerprint(self, fingerprint: str) -> bool:
        """Delete a drift monitor state by fingerprint"""
        pass