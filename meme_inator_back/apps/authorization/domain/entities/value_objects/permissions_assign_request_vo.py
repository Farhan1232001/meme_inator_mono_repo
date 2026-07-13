from dataclasses import dataclass


@dataclass
class PermissionAssignRequest:
    permission_slug: str