# application/usecases/direct_for_human_moderation.py
from uuid import UUID
from apps.moderation_sys.domain.enums.moderation_enums import DecisionEnum, ModerationActionEnum, VisibilityEffectEnum
from apps.moderation_sys.domain.irepositories.moderation_case_repository import IModerationCaseRepository
from apps.moderation_sys.domain.value_objects.moderation_action import ModerationActionVo
from apps.moderation_sys.domain.value_objects.moderation_decision import ModerationDecisionVo
from core.results import Result, Ok, NotOk, Error

class DirectContentForHumanModerationUsecase:
    """Human reviewing content for approval - BP#2"""
    
    def __init__(self, case_repo: IModerationCaseRepository):
        self.case_repo = case_repo

    def execute(
        self, 
        case_id: UUID, 
        decision: str, 
        moderator_id: UUID, 
        note: str = None
    ) -> Result:
        """Direct content to human moderation queue or process human decision"""
        try:
            case = self.case_repo.find_by_id(case_id)
            if not case:
                return NotOk(message="Case not found", static_msg="CASE_NOT_FOUND")
            
            # Convert string decision to enum
            try:
                decision_enum = DecisionEnum(decision.upper())
            except ValueError:
                return NotOk(message="Invalid decision", static_msg="INVALID_DECISION")
            
            # Create decision VO
            moderation_decision = ModerationDecisionVo(
                outcome=decision_enum,
                note=note
            )
            
            # Create corresponding action
            if decision_enum == DecisionEnum.ACCEPT:
                action = ModerationActionVo(
                    action_type=ModerationActionEnum.ACCEPT,
                    visibility_effect=VisibilityEffectEnum.IMMEDIATE,
                    reason=f"Human moderator approved: {note or 'No note provided'}"
                )
            elif decision_enum == DecisionEnum.REJECT:
                action = ModerationActionVo(
                    action_type=ModerationActionEnum.REJECT,
                    visibility_effect=VisibilityEffectEnum.IMMEDIATE,
                    reason=f"Human moderator rejected: {note or 'No note provided'}"
                )
            else:  # FLAG
                action = ModerationActionVo(
                    action_type=ModerationActionEnum.FLAG,
                    visibility_effect=VisibilityEffectEnum.DELAYED,
                    reason=f"Human moderator flagged: {note or 'No note provided'}"
                )
            
            case.human_moderate(moderation_decision, moderator_id, note)
            case.action = action
            saved_case = self.case_repo.save(case)
            
            return Ok(value=saved_case)
            
        except ValueError as e:
            return NotOk(message=str(e), static_msg="VALIDATION_ERROR")
        except Exception as e:
            return Error(message="Failed to process human moderation", exception=e)