from typing import List, Optional
from uuid import UUID
from ninja import Schema
# ------------

class RoleResponseSchema(Schema):
    id: int
    name: str

class ListRolesResponseSchema(Schema):
    roles: List[RoleResponseSchema]


# ------------



class PermissionResponseSchema(Schema):
    id: int
    codename: str
    name: str
    app_label: Optional[str] = None

class PermissionsListResponseSchema(Schema):
    permissions: List[PermissionResponseSchema]


# ------------


    
class CanPermissionRequestSchema(Schema):
    user_id: str
    action: str

class CanPermissionResponseSchema(Schema):
    user_id: str
    action: str
    authorized: bool


# ------------


class AssignPermissionToRoleRequestSchema(Schema):
    role_id: UUID
    permission_slug: str

class AssignPermissionToRoleResponseSchema(Schema):
    role_id: UUID
    permission_slug: str
    is_sucessful: bool

# ------------
class RemovePermissionToRoleRequestSchema(Schema):
    role_id: UUID
    permission_slug: str

class RemovePermissionToRoleResponseSchema(Schema):
    role_id: UUID
    permission_slug: str
    is_successful: bool