# apps/profiles/application/dtos/profile_with_followship_context.py
from .profile_schema import ProfileSchema

class ProfileWithFollowshipContext(ProfileSchema):
    is_following: bool = False