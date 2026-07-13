# domain/irepositories/policy_definition_repository.py
from abc import ABC, abstractmethod
from uuid import UUID
from typing import Dict, Optional, List, Tuple

from apps.moderation_sys.domain.aggregates.policy_definition import PolicyDefinition

class IPolicyDefinitionRepository(ABC):
    @abstractmethod
    def save(self, policy: PolicyDefinition) -> PolicyDefinition:
        """Save or update a policy definition"""
        pass
    
    @abstractmethod
    def bulk_save(self, policies: List[PolicyDefinition]) -> int:
        """Bulk insert new policies. Returns count of created policies."""
        pass

    @abstractmethod
    def find_by_id(self, policy_id: UUID) -> Optional[PolicyDefinition]:
        """Find policy by its ID"""
        pass

    @abstractmethod
    def find_active_policy_via_routing_key(self, routing_key: str) -> Optional[PolicyDefinition]:
        """Find the currently active policy for a given routing key"""
        pass

    @abstractmethod
    def find_all_active(self) -> List[PolicyDefinition]:
        """Find all currently active policies"""
        pass

    @abstractmethod
    def find_by_routing_key(self, routing_key: str) -> List[PolicyDefinition]:
        """Find all policies (including inactive) for a routing key"""
        pass

    @abstractmethod
    def find_latest_version(self, routing_key: str) -> Optional[PolicyDefinition]:
        """Find the latest version of a policy for a routing key"""
        pass

    @abstractmethod
    def existing_versions(self, pairs: List[Tuple[str, int]]) -> Dict[Tuple[str, int], PolicyDefinition]:
        """
        Given a list of policy definition identifiers such that an identifier is the tuple (routing_key, version).
        return a dict mapping identifier to the PolicyDefinition
            such that for all identifiers that currently exist in the database.
        """
        pass