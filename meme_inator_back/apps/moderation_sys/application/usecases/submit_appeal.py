# application/usecases/submit_appeal.py
from uuid import UUID
from apps.moderation_sys.domain.irepositories.moderation_case_repository import IModerationCaseRepository
from apps.moderation_sys.domain.services.policy_registry_service import PolicyRegistryService
from core.results import Result, Ok, NotOk, Error

class SubmitAppealUsecase:
    def __init__(self, case_repo: IModerationCaseRepository, policy_registry: PolicyRegistryService):
        self.case_repo = case_repo
        self.policy_registry = policy_registry

    def execute(self, case_id: UUID, user_id: UUID, reason: str) -> Result:
        try:
            case = self.case_repo.find_by_id(case_id)
            if not case:
                return NotOk(message="Case not found", static_msg="CASE_NOT_FOUND")

            # Get policy for this case
            policy = self.policy_registry.lookup_active_policy(case.content.policy_routing_key)

            # Check eligibility
            user_history = {}  # fetch from user repo
            if not policy.is_appeal_eligible(case, user_history):
                return NotOk(message="Appeal not eligible", static_msg="APPEAL_NOT_ELIGIBLE")

            case.submit_appeal(user_id, reason, policy.appeal_eligibility_rules)
            self.case_repo.save(case)

            return Ok(value=case.appeal)
        except ValueError as e:
            return NotOk(message=str(e), static_msg="INVALID_APPEAL")
        except Exception as e:
            return Error(message="Failed to submit appeal", exception=e)