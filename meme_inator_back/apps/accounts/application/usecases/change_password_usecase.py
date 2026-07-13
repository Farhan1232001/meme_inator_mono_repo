from uuid import UUID
from core.results import Ok, NotOk, Error, Result

from apps.accounts.domain.iusecases.ichange_password_usecase import (
    IChangePasswordUsecase,
)
from apps.accounts.domain.irepositories.ipassword_change_repository import (
    IPasswordChangeRepository,
)


class ChangePasswordUsecase(IChangePasswordUsecase):
    """
    Authenticated password change usecase.
    """

    def __init__(self, password_repo: IPasswordChangeRepository):
        self._password_repo = password_repo

    def change_password(
        self,
        *,
        user_id: UUID,
        current_password: str,
        new_password: str,
    ) -> Result[None]:

        if current_password == new_password:
            return NotOk(
                message="new password must be different",
                static_msg="PASSWORD_UNCHANGED",
                status_code=400,
            )

        # 1️⃣ Verify current password
        verify_result = self._password_repo.verify_current_password(
            user_id=user_id,
            current_password=current_password,
        )

        if not isinstance(verify_result, Ok):
            return verify_result

        # 2️⃣ Set new password
        set_result = self._password_repo.set_new_password(
            user_id=user_id,
            new_password=new_password,
        )

        if not isinstance(set_result, Ok):
            return set_result

        return Ok(None)
