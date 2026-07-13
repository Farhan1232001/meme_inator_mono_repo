# infrastructure/services/yaml_policy_loader.py
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import yaml
from pathlib import Path
from apps.moderation_sys.domain.aggregates.policy_definition import PolicyDefinition
from apps.moderation_sys.domain.enums.moderation_enums import DecisionEnum
from apps.moderation_sys.domain.irepositories.policy_definition_repository import IPolicyDefinitionRepository
from apps.moderation_sys.domain.value_objects.appeal_eligibility_rules import AppealEligibilityRulesVo
from apps.moderation_sys.domain.value_objects.confidence_thresholds import ConfidenceThresholdsVo
from apps.moderation_sys.domain.value_objects.drift_detection_policy import DriftDetectionPolicyVo
from apps.moderation_sys.domain.value_objects.reputation_impact import ReputationImpactVo
from apps.moderation_sys.domain.value_objects.webhook_retry_policy import WebhookRetryPolicyVo

class YamlPolicyLoader:
    def __init__(self, repo: IPolicyDefinitionRepository):
        self.repo = repo

    def load_from_file(self, path: Path) -> PolicyDefinition:
        with open(path) as f:
            data = yaml.safe_load(f)

        appealable_decisions = [DecisionEnum(d) for d in data['appeal_eligibility']['appealable_decisions']]

        # Updated to use new field names from your ConfidenceThresholdsVo
        high_risk = data['confidence_thresholds']['high_risk_threshold']
        low_risk = data['confidence_thresholds']['low_risk_threshold']
        grey_zone = data['confidence_thresholds']['grey_zone_min']
        
        thresholds = ConfidenceThresholdsVo(
            high_risk_threshold=high_risk,
            low_risk_threshold=low_risk,
            grey_zone_min=grey_zone,
        )

        # Parse datetime strings to datetime objects
        active_from = data.get('active_from')
        if isinstance(active_from, str):
            active_from = datetime.fromisoformat(active_from.replace('Z', '+00:00'))
        
        active_to = data.get('active_to')
        if isinstance(active_to, str):
            active_to = datetime.fromisoformat(active_to.replace('Z', '+00:00'))

        policy = PolicyDefinition(
            routing_key=data['routing_key'],
            version=data.get('version', 1),
            active_from=active_from,
            active_to=active_to,
            confidence_thresholds=thresholds,
            appeal_eligibility_rules=AppealEligibilityRulesVo(
                time_limit_hours=data['appeal_eligibility']['time_limit_hours'],
                requires_reason=data['appeal_eligibility']['requires_reason'],
                appealable_decisions=appealable_decisions,
                max_appeals_per_user_per_day=data['appeal_eligibility']['max_appeals_per_user_per_day'],
            ),
            reputation_impact=ReputationImpactVo(
                accept_points_delta=data['reputation_impact']['accept_points'],
                reject_points_delta=data['reputation_impact']['reject_points'],
                appeal_upheld_points_return=data['reputation_impact']['appeal_upheld_return'],
                appeal_denied_penalty=data['reputation_impact']['appeal_denied_penalty'],
            ),
            webhook_retry_policy=WebhookRetryPolicyVo(**data['webhook_retry']),
            drift_detection_policy=DriftDetectionPolicyVo(**data['drift_detection']),
        )
        return policy

    def sync_directory(self, policies_dir: Path) -> int:
        """Idempotent sync: update or insert policies based on routing_key+version."""

        # 1. Collect all YAML file paths. each yaml file stores a PolicyDefinition
        yaml_files = list(policies_dir.rglob("*.yaml")) + list(policies_dir.rglob("*.yml"))

        # 2. Load all policies from YAML
        yaml_policies: List[PolicyDefinition] = []
        for file_path in yaml_files:
            try:
                policy = self.load_from_file(file_path)
                yaml_policies.append(policy)
            except Exception as e:
                raise RuntimeError(f"Failed to load policy from {file_path}: {e}")

        if not yaml_policies:
            return 0

        # 3. Build list of identifiers ie (routing_key, version) pairs to check in DB
        # Identifier == (routing_key, policy version)
        identifiers = [(p.routing_key, p.version) for p in yaml_policies]

        # 4. Fetch existing policies from database in one query
        existing_map: Dict[Tuple[str, int], PolicyDefinition] = self.repo.existing_versions(identifiers) 

        # 5. Determine which YAML policies are new
        new_policies: List[PolicyDefinition] = []
        for policy in yaml_policies:
            key = (policy.routing_key, policy.version)
            if key not in existing_map:
                new_policies.append(policy)

        if len(new_policies) == 0:
            return 0

        # 6. Bulk save new policies
        saved_count = self.repo.bulk_save(new_policies)

        return saved_count