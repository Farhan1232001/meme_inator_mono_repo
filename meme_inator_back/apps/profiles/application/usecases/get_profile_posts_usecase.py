from typing import Dict, Any, Optional
from uuid import UUID
from apps.profiles.domain.usecases.iget_profile_posts_usecase import IGetProfilePostsUsecase
from apps.profiles.domain.irepositories.i_profile_repository import IProfileRepository
from core.results import Result

class GetProfilePostsUsecase(IGetProfilePostsUsecase):
    def __init__(self, profile_repo: IProfileRepository):
        self.profile_repo = profile_repo

    def execute(self, username: str, cursor: Optional[str] = None, page_size: int = 10) -> Result[Dict[str, Any]]:
        # The repository returns a Result containing a dict with 'posts' and 'next_cursor'
        return self.profile_repo.get_profile_posts(username, cursor, page_size)
    