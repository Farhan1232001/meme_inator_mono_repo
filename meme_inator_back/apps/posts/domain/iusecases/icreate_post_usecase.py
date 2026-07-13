# apps/posts/domain/iusecases/icreate_post_usecase.py
from abc import ABC, abstractmethod

from apps.posts.domain.entities.post_data_vo import PostDataVo
from core.results import Result
from apps.posts.domain.entities.post_entity import PostEntity


class ICreatePostUsecase(ABC):
    """Interface for creating a new post."""
    
    @abstractmethod
    def execute(self, post_data: PostDataVo) -> Result[PostEntity]:
        """Create a new post with the given data."""
        ...