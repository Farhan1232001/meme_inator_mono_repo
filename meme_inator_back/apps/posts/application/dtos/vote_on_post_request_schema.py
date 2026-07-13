# apps/posts/application/dtos/schemas.py
from typing import Optional
from uuid import UUID
from ninja import Schema
from apps.commentsections.domain.enums.vote_action_enum import VoteActionEnum


class VoteOnPostRequestSchema(Schema):
    action: VoteActionEnum