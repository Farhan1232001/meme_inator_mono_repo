from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List

from apps.posts.domain.irepositories.iposts_repository import IPostRepository

class IGetProfilePostsUsecase(ABC):
    """
    Attributes:
        - post_repo: IPostRepository
    Returns:
        { "next_cursor" : Optional[str], "results": List[PostEntity] }
    """

    def __init__(self, post_repo: IPostRepository) -> None:
        self.post_repo = post_repo

    @abstractmethod
    def execute(self, username: str, cursor: Optional[str] = None, page_size: int = 10) -> Dict[str, Any]:
        """Fetch paginated posts for a public profile."""
        raise NotImplementedError