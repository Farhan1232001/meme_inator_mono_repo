# apps/posts/models.py
from apps.posts.infrastructure.models.post_model import PostModel
from apps.posts.infrastructure.models.post_vote_model import PostVoteModel

__all__ = ["PostModel", "PostVoteModel"]

