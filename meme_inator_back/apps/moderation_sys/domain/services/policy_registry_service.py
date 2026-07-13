# domain/services/policy_registry_service.py
from functools import lru_cache

from apps.moderation_sys.domain.aggregates.policy_definition import PolicyDefinition
from apps.moderation_sys.domain.irepositories.policy_definition_repository import IPolicyDefinitionRepository

class PolicyRegistryService:
    """
    
    How it works?
        Uses longest prefix match algorithm.

    TODO:
    How to optimize?
        1. trie-based approach IF many active policies (100+) and performance is critical and policies dont change frequently (rebuild on policy changes)
        2. cached prefix lookup IF simplicity is important. Policy changes are rare. 
            use lru_cache decorator. Aka memoize approach. 
        3. Hash map key, value = policy routing key, PolicyDefinition
        4. DB-level matching IF real-time policy updates needed and databse query performance is acceptable. 
        5. Regex-based with precompiled patterns appoach IF text is complex. 
    """
    def __init__(self, policy_def_repo: IPolicyDefinitionRepository):
        self._policy_def_repo = policy_def_repo

    # TODO: Increase cache IF needed.
    # Make algo more efficent. Use regex. 
    @lru_cache(maxsize=64)
    def lookup_active_policy(self, routing_key: str) -> PolicyDefinition:

        # Split the routing key into parts: e.g., "channel:namespace:type" -> ["channel", "namespace", "type"]
        routing_parts = routing_key.split(':')
        # Try to find an active policy starting from the most specific key down to less specific
        for i in range(len(routing_parts), 0, -1):
            current_key = ':'.join(routing_parts[:i])
            policy = self._policy_def_repo.find_active_policy_via_routing_key(current_key)
            if policy:
                return policy
            
        # If no specific policy found, return the global default
        return self._policy_def_repo.find_active_policy_via_routing_key("mod_sys:global_default")