# application/usecases/notify_user_of_moderated_content.py
from uuid import UUID
from apps.moderation_sys.domain.enums.moderation_enums import CaseStatusEnum
from apps.moderation_sys.domain.irepositories.moderation_case_repository import IModerationCaseRepository
from core.results import Result, Ok, NotOk, Error

class NotifyUserOfModeratedContentUsecase:
    """Notify user about moderation decision"""
    
    def __init__(self, case_repo: IModerationCaseRepository):
        self.case_repo = case_repo
        # In real implementation, inject notification service

    def execute(self, case_id: UUID) -> Result:
        """Send notification to user about moderation decision"""
        try:
            case = self.case_repo.find_by_id(case_id)
            if not case:
                return NotOk(message="Case not found", static_msg="CASE_NOT_FOUND")
            
            if case.status not in [CaseStatusEnum.RESOLVED, CaseStatusEnum.ACCEPTED]:
                return NotOk(message="Case not in notifiable state", static_msg="CASE_NOT_NOTIFIABLE")
            
            # Prepare notification based on decision
            notification_data = {
                "user_id": str(case.content.author_id),
                "content_id": str(case.content.content_id),
                "decision": case.decision.outcome.value if case.decision else "UNKNOWN",
                "reason": case.decision.reason_code if case.decision else None,
                "can_appeal": case.decision.outcome == "REJECT" if case.decision else False,
                "case_id": str(case.case_id)
            }
            
            # TODO: Actually send notification via notification service
            # notification_service.send(user_id, template, notification_data)
            
            # Log notification
            print(f"Notification would be sent: {notification_data}")
            
            return Ok(value={
                "notified": True,
                "case_id": str(case.case_id),
                "notification_data": notification_data
            })
            
        except Exception as e:
            return Error(message="Failed to send notification", exception=e)