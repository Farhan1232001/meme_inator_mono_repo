# application/usecases/update_policy.py
from datetime import datetime, timezone
from uuid import UUID
from apps.moderation_sys.domain.enums.moderation_enums import DecisionEnum
from apps.moderation_sys.domain.irepositories.policy_definition_repository import IPolicyDefinitionRepository
from apps.moderation_sys.domain.value_objects.appeal_eligibility_rules import AppealEligibilityRulesVo
from apps.moderation_sys.domain.value_objects.confidence_thresholds import ConfidenceThresholdsVo
from apps.moderation_sys.domain.value_objects.reputation_impact import ReputationImpactVo
from core.results import Result, Ok, NotOk, Error

class UpdatePolicyUsecase:
    """Update moderation policy - BP#9"""
    
    def __init__(self, policy_repo: IPolicyDefinitionRepository):
        self.policy_repo = policy_repo

    def execute(
        self, 
        policy_id: UUID, 
        admin_id: UUID, 
        updates: dict
    ) -> Result:
        """Update policy rules"""
        try:
            policy = self.policy_repo.find_by_id(policy_id)
            if not policy:
                return NotOk(message="Policy not found", static_msg="POLICY_NOT_FOUND")
            
            # Apply updates based on what's provided
            if "confidence_thresholds" in updates:
                thresholds_data = updates["confidence_thresholds"]
                # FIXED: Use new parameter names (high_risk_threshold, low_risk_threshold)
                # Map old field names to new ones if they exist
                high_risk = thresholds_data.get("high_risk_threshold", 
                            thresholds_data.get("high_confidence_min", 0.7))
                low_risk = thresholds_data.get("low_risk_threshold",
                           thresholds_data.get("low_confidence_max", 0.3))
                
                new_thresholds = ConfidenceThresholdsVo(
                    high_risk_threshold=high_risk,
                    low_risk_threshold=low_risk,
                    grey_zone_min=low_risk  # Must equal low_risk_threshold
                )
                policy.update_thresholds(new_thresholds, admin_id)
            
            if "appeal_rules" in updates:
                rules_data = updates["appeal_rules"]
                # Convert string decisions to enum
                appealable = [
                    DecisionEnum(d) for d in rules_data.get("appealable_decisions", ["REJECT"])
                ]
                new_rules = AppealEligibilityRulesVo(
                    time_limit_hours=rules_data.get("time_limit_hours", 48),
                    requires_reason=rules_data.get("requires_reason", True),
                    appealable_decisions=appealable,
                    max_appeals_per_user_per_day=rules_data.get("max_appeals_per_user_per_day", 3)
                )
                policy.update_appeal_rules(new_rules, admin_id)
            
            if "reputation_impact" in updates:
                impact_data = updates["reputation_impact"]
                new_impact = ReputationImpactVo(
                    accept_points_delta=impact_data.get("accept_points_change", 10),
                    reject_points_delta=impact_data.get("rejected_points_change", -25),
                    appeal_upheld_points_return=impact_data.get("appeal_upheld_points_return", 25),
                    appeal_denied_penalty=impact_data.get("appeal_denied_penalty", -10)
                )
                policy.reputation_impact = new_impact
                policy.updated_at = datetime.now(timezone.utc)
                policy.version += 1
            
            # Save updated policy
            saved_policy = self.policy_repo.save(policy)
            
            return Ok(value=saved_policy)
            
        except ValueError as e:
            return NotOk(message=str(e), static_msg="VALIDATION_ERROR")
        except Exception as e:
            return Error(message="Failed to update policy", exception=e)