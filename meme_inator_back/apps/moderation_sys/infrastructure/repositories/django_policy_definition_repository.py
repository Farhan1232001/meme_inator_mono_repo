# infrastructure/repositories/django_policy_definition_repository.py
from uuid import UUID
from typing import Dict, Optional, List, Tuple
from datetime import datetime, timezone

from django.db.models import Q

from apps.moderation_sys.domain.aggregates.policy_definition import PolicyDefinition
from apps.moderation_sys.domain.enums.moderation_enums import DecisionEnum
from apps.moderation_sys.domain.irepositories.policy_definition_repository import IPolicyDefinitionRepository
from apps.moderation_sys.domain.value_objects.appeal_eligibility_rules import AppealEligibilityRulesVo
from apps.moderation_sys.domain.value_objects.confidence_thresholds import ConfidenceThresholdsVo
from apps.moderation_sys.domain.value_objects.drift_detection_policy import DriftDetectionPolicyVo
from apps.moderation_sys.domain.value_objects.reputation_impact import ReputationImpactVo
from apps.moderation_sys.domain.value_objects.webhook_retry_policy import WebhookRetryPolicyVo
from apps.moderation_sys.infrastructure.models.policy_definition_model import PolicyDefinitionModel



class DjangoPolicyDefinitionRepository(IPolicyDefinitionRepository):
    """
    SSOT for PolicyDefinitions. Policy definition can be active or inactive. Getter methods for that ack both active/inactive policies. 
    """
    
    def save(self, policy: PolicyDefinition) -> PolicyDefinition:
        """Save or update a policy definition"""
        # FIXED: Use properties high_confidence_min and low_confidence_max instead of direct attribute access
        model, created = PolicyDefinitionModel.objects.update_or_create(
            policy_id=policy.policy_id,
            defaults={
                'routing_key': policy.routing_key,
                'version': policy.version,
                'high_confidence_min': policy.confidence_thresholds.high_confidence_min,  # Using property
                'low_confidence_max': policy.confidence_thresholds.low_confidence_max,    # Using property
                'grey_zone_min': policy.confidence_thresholds.grey_zone_min,
                'appeal_rules': {
                    'time_limit_hours': policy.appeal_eligibility_rules.time_limit_hours,
                    'requires_reason': policy.appeal_eligibility_rules.requires_reason,
                    'appealable_decisions': [d.value for d in policy.appeal_eligibility_rules.appealable_decisions],
                    'max_appeals_per_user_per_day': policy.appeal_eligibility_rules.max_appeals_per_user_per_day,
                },
                'reputation_impact': {
                    'accept_points_change': policy.reputation_impact.accept_points_delta,
                    'rejected_points_change': policy.reputation_impact.reject_points_delta,
                    'appeal_upheld_points_return': policy.reputation_impact.appeal_upheld_points_return,
                    'appeal_denied_penalty': policy.reputation_impact.appeal_denied_penalty,
                },
                'webhook_retry_policy': {
                    'max_retries': policy.webhook_retry_policy.max_retries,
                    'initial_delay_seconds': policy.webhook_retry_policy.initial_delay_seconds,
                    'backoff_multiplier': policy.webhook_retry_policy.backoff_multiplier,
                    'max_delay_seconds': policy.webhook_retry_policy.max_delay_seconds,
                },
                'drift_detection_policy': {
                    'confidence_delta_threshold': policy.drift_detection_policy.confidence_delta_threshold,
                    'decision_change_required': policy.drift_detection_policy.decision_change_required,
                    'min_samples': policy.drift_detection_policy.min_samples,
                },
                'active_from': policy.active_from,
                'active_to': policy.active_to,
                'updated_at': policy.updated_at,
            }
        )
        return self._to_domain(model)
    
    def bulk_save(self, policies: List[PolicyDefinition]) -> int:
        """Bulk insert new policies. Returns count of created policies."""
        if not policies:
            return 0
        
        models = []
        for policy in policies:
            # FIXED: Use properties high_confidence_min and low_confidence_max
            models.append(PolicyDefinitionModel(
                policy_id=policy.policy_id,
                routing_key=policy.routing_key,
                version=policy.version,
                high_confidence_min=policy.confidence_thresholds.high_confidence_min,
                low_confidence_max=policy.confidence_thresholds.low_confidence_max,
                grey_zone_min=policy.confidence_thresholds.grey_zone_min,
                appeal_rules={
                    'time_limit_hours': policy.appeal_eligibility_rules.time_limit_hours,
                    'requires_reason': policy.appeal_eligibility_rules.requires_reason,
                    'appealable_decisions': [d.value for d in policy.appeal_eligibility_rules.appealable_decisions],
                    'max_appeals_per_user_per_day': policy.appeal_eligibility_rules.max_appeals_per_user_per_day,
                },
                reputation_impact={
                    'accept_points_delta': policy.reputation_impact.accept_points_delta,
                    'reject_points_delta': policy.reputation_impact.reject_points_delta,
                    'appeal_upheld_points_return': policy.reputation_impact.appeal_upheld_points_return,
                    'appeal_denied_penalty': policy.reputation_impact.appeal_denied_penalty,
                },
                webhook_retry_policy={
                    'max_retries': policy.webhook_retry_policy.max_retries,
                    'initial_delay_seconds': policy.webhook_retry_policy.initial_delay_seconds,
                    'backoff_multiplier': policy.webhook_retry_policy.backoff_multiplier,
                    'max_delay_seconds': policy.webhook_retry_policy.max_delay_seconds,
                },
                drift_detection_policy={
                    'confidence_delta_threshold': policy.drift_detection_policy.confidence_delta_threshold,
                    'decision_change_required': policy.drift_detection_policy.decision_change_required,
                    'min_samples': policy.drift_detection_policy.min_samples,
                },
                active_from=policy.active_from,
                active_to=policy.active_to,
                updated_at=policy.updated_at,
            ))
        
        created = PolicyDefinitionModel.objects.bulk_create(
            models,
            ignore_conflicts=True,  # Postgres only
            batch_size=500,
        )
        return len(created)

    def find_by_id(self, policy_id: UUID) -> Optional[PolicyDefinition]:
        """Find policy by its ID"""
        try:
            model = PolicyDefinitionModel.objects.get(policy_id=policy_id)
            return self._to_domain(model)
        except PolicyDefinitionModel.DoesNotExist:
            return None
    
    def find_active_policy_via_routing_key(self, routing_key: str) -> Optional[PolicyDefinition]:
        """Find the currently active policy for a given routing key"""
        now = datetime.now(timezone.utc)
        try:
            model = PolicyDefinitionModel.objects.filter(
                routing_key=routing_key,
                active_from__lte=now
            ).filter(
                Q(active_to__isnull=True) | Q(active_to__gt=now)
            ).order_by('-version').first()
            
            if model:
                return self._to_domain(model)
            return None
        except PolicyDefinitionModel.DoesNotExist:
            return None
    
    def find_all_active(self) -> List[PolicyDefinition]:
        """Find all currently active policies"""
        now = datetime.now(timezone.utc)
        models = PolicyDefinitionModel.objects.filter(
            active_from__lte=now
        ).filter(
            Q(active_to__isnull=True) | Q(active_to__gt=now)
        ).order_by('routing_key', '-version').distinct('routing_key')
        
        return [self._to_domain(model) for model in models]
    
    def find_by_routing_key(self, routing_key: str) -> List[PolicyDefinition]:
        """Find all policies (including inactive) for a routing key"""
        models = PolicyDefinitionModel.objects.filter(
            routing_key=routing_key
        ).order_by('-version')
        
        return [self._to_domain(model) for model in models]
    
    def find_latest_version(self, routing_key: str) -> Optional[PolicyDefinition]:
        """Find the latest version of a policy for a routing key"""
        try:
            model = PolicyDefinitionModel.objects.filter(
                routing_key=routing_key
            ).order_by('-version').first()
            
            if model:
                return self._to_domain(model)
            return None
        except PolicyDefinitionModel.DoesNotExist:
            return None
    
    def existing_versions(self, identifiers: List[Tuple[str, int]]) -> Dict[Tuple[str, int], PolicyDefinition]:
        """
        TODO: Can query be made more efficient?
        """
        if not identifiers:
            return {}

        # Build a complex Q filter to match (routing_key, version) combos
        q = Q()
        for routing_key, version in identifiers:
            q |= Q(routing_key=routing_key, version=version)

        models = PolicyDefinitionModel.objects.filter(q)

        result = {}
        for model in models:
            result[(model.routing_key, model.version)] = self._to_domain(model)
        return result

    def _to_domain(self, model: PolicyDefinitionModel) -> PolicyDefinition:
        """Convert model to domain aggregate"""
        # FIXED: Use new parameter names (high_risk_threshold, low_risk_threshold)
        # Map the stored high_confidence_min to high_risk_threshold
        confidence_thresholds = ConfidenceThresholdsVo(
            high_risk_threshold=model.high_confidence_min,
            low_risk_threshold=model.low_confidence_max,
            grey_zone_min=model.grey_zone_min
        )
        
        appeal_rules_data = model.appeal_rules
        appeal_eligibility_rules = AppealEligibilityRulesVo(
            time_limit_hours=appeal_rules_data.get('time_limit_hours', 24),
            requires_reason=appeal_rules_data.get('requires_reason', True),
            appealable_decisions=[DecisionEnum(d) for d in appeal_rules_data.get('appealable_decisions', ['REJECT'])],
            max_appeals_per_user_per_day=appeal_rules_data.get('max_appeals_per_user_per_day', 3)
        )
        
        reputation_data = model.reputation_impact
        reputation_impact = ReputationImpactVo(
            accept_points_delta=reputation_data.get('accept_points_change', 10),
            reject_points_delta=reputation_data.get('rejected_points_change', -25),
            appeal_upheld_points_return=reputation_data.get('appeal_upheld_points_return', 25),
            appeal_denied_penalty=reputation_data.get('appeal_denied_penalty', -10)
        )
        
        webhook_data = model.webhook_retry_policy
        webhook_retry_policy = WebhookRetryPolicyVo(
            max_retries=webhook_data.get('max_retries', 5),
            initial_delay_seconds=webhook_data.get('initial_delay_seconds', 60),
            backoff_multiplier=webhook_data.get('backoff_multiplier', 2.0),
            max_delay_seconds=webhook_data.get('max_delay_seconds', 3600)
        )
        
        drift_data = model.drift_detection_policy
        drift_detection_policy = DriftDetectionPolicyVo(
            confidence_delta_threshold=drift_data.get('confidence_delta_threshold', 0.2),
            decision_change_required=drift_data.get('decision_change_required', False),
            min_samples=drift_data.get('min_samples', 5)
        )
        
        return PolicyDefinition(
            policy_id=model.policy_id,
            routing_key=model.routing_key,
            version=model.version,
            confidence_thresholds=confidence_thresholds,
            appeal_eligibility_rules=appeal_eligibility_rules,
            reputation_impact=reputation_impact,
            webhook_retry_policy=webhook_retry_policy,
            drift_detection_policy=drift_detection_policy,
            active_from=model.active_from,
            active_to=model.active_to,
            updated_at=model.updated_at
        )