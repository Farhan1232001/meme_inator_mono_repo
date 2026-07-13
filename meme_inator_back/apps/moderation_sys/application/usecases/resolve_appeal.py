# application/usecases/resolve_appeal.py
from uuid import UUID
from apps.moderation_sys.domain.enums.moderation_enums import AppealOutcomeEnum, DecisionEnum, ModerationActionEnum, VisibilityEffectEnum
from apps.moderation_sys.domain.irepositories.moderation_case_repository import IModerationCaseRepository
from apps.moderation_sys.domain.value_objects.moderation_action import ModerationActionVo
from apps.moderation_sys.domain.value_objects.moderation_decision import ModerationDecisionVo
from core.results import Result, Ok, NotOk, Error


class ResolveAppealUsecase:
    """Resolve an appeal - BP#4"""
    
    def __init__(self, case_repo: IModerationCaseRepository):
        self.case_repo = case_repo

    def execute(
        self, 
        case_id: UUID, 
        outcome: str, 
        moderator_id: UUID, 
        resolution_note: str = None
    ) -> Result:
        """Resolve a pending appeal"""
        try:
            case = self.case_repo.find_by_id(case_id)
            if not case:
                return NotOk(message="Case not found", static_msg="CASE_NOT_FOUND")
            
            if not case.appeal:
                return NotOk(message="No appeal found for this case", static_msg="NO_APPEAL_FOUND")
            
            if case.appeal.status != "PENDING":
                return NotOk(message="Appeal is not pending", static_msg="APPEAL_NOT_PENDING")
            
            # Convert string outcome to enum
            try:
                outcome_enum = AppealOutcomeEnum(outcome.upper())
            except ValueError:
                return NotOk(message="Invalid outcome", static_msg="INVALID_OUTCOME")
            
            # Resolve the appeal
            case.resolve_appeal(outcome_enum, moderator_id, resolution_note)
            
            # If appeal approved, update the decision
            if outcome_enum == AppealOutcomeEnum.APPROVED:
                # Reverse the original rejection
                case.decision = ModerationDecisionVo(
                    outcome=DecisionEnum.ACCEPT,
                    reason_code="APPEAL_APPROVED",
                    note=f"Appeal approved: {resolution_note or 'No note provided'}"
                )
                case.action = ModerationActionVo(
                    action_type=ModerationActionEnum.ACCEPT,
                    visibility_effect=VisibilityEffectEnum.IMMEDIATE,
                    reason="Appeal approved - content accepted"
                )
            
            saved_case = self.case_repo.save(case)
            
            # TODO: Update reputation based on appeal outcome
            # This would call a reputation service
            
            return Ok(value=saved_case)
            
        except ValueError as e:
            return NotOk(message=str(e), static_msg="VALIDATION_ERROR")
        except Exception as e:
            return Error(message="Failed to resolve appeal", exception=e)