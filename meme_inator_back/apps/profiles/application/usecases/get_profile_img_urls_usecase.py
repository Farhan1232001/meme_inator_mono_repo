from typing import Dict
from uuid import UUID
from apps.profiles.domain.usecases.iget_profile_img_urls_usecase import IGetProfileImageUrlsUsecase
from apps.profiles.domain.irepositories.i_profile_repository import IProfileRepository
from core.results import Result

class GetProfileImageUrlsUsecase(IGetProfileImageUrlsUsecase):
    def __init__(self, profile_repo: IProfileRepository):
        self.profile_repo = profile_repo

    def execute(self, user_id: UUID) -> Result[Dict[str, str]]:
        return self.profile_repo.get_profile_image_urls(user_id)