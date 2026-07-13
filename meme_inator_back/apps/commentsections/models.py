# This file serves as the entry point for Django's model discovery
from .infrastructure.models.comments_model import CommentModel
from .infrastructure.models.comment_vote_model import CommentVoteModel

# This ensures Django includes the model in migrations
__all__ = ["CommentModel", "CommentVoteModel"]