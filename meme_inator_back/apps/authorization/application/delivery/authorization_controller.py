
from typing import Any, Dict, List, Optional
from uuid import UUID
from ninja_extra import http_delete, http_get, http_post, api_controller, route
from django.http import HttpRequest
from ninja_jwt.authentication import JWTAuth
from django.contrib.auth.models import Group, Permission
from django.shortcuts import get_object_or_404
from apps.authorization.application.orchestration.authz_orchestration import AuthorizationOrchestration
from apps.authorization.domain.entities.permission_entity import PermissionEntity
from apps.authorization.domain.entities.role_entity import RoleEntity
from apps.authorization.domain.entities.value_objects.can_permission_response_vo import CanPermissionResponseVo
from apps.users.models import UserModel
from apps.authorization.application.dtos.schemas import AssignPermissionToRoleRequestSchema, AssignPermissionToRoleResponseSchema, CanPermissionRequestSchema, ListRolesResponseSchema, PermissionResponseSchema, CanPermissionResponseSchema, PermissionsListResponseSchema, RemovePermissionToRoleRequestSchema, RemovePermissionToRoleResponseSchema, RoleResponseSchema
from core.dtos.results_schemas import ErrorResponseSchema
from core.results import Ok, NotOk, Error, Result
from meme_inator_back import settings
from core.dependency_injections import di

@api_controller('/authz', tags=['authorization'])
class AuthorizationController:
    """
    Controller exposing authorization endpoints. Each method currently raises NotImplementedError.
    Wire this controller to your routing (Django-Ninja / ninja_extra) and call orchestration methods.
    """

    def __init__(self):
        self.authz_orchestration = di.create_authorization_orchestration()
    
    @route.get(
        '/roles',
        tags=['authz'],
        auth=JWTAuth(),
        permissions=None,
        response={
            200: ListRolesResponseSchema,
        }
    )
    def list_roles(self):
        """List all available roles in the system"""
        # 1. Get roles
        roles_list_result:Result[List[RoleEntity]] = self.authz_orchestration.get_roles_list()

        # parse result
        match roles_list_result:
            case Ok(value=roles_list):
                return 200, ListRolesResponseSchema(
                    roles=roles_list
                )

            case Error(message=message, static_msg=static_msg, exception=exception, status_code=status_code):
                # debug mode returns detailed message, otherwise return generic vague message
                if settings.DEBUG:
                    return status_code, ErrorResponseSchema(
                        message=message, 
                        static_msg=static_msg, 
                        exception_str=str(exception)
                    )
                else:
                    return status_code, ErrorResponseSchema(message='internal server error')

            case _:
                return 500, ErrorResponseSchema(detail="unexpected result", code="INTERNAL_ERROR")

    @route.get(
        '/permissions',
        tags=['authz'],
        auth=JWTAuth(),
        permissions=None,
        response={
            200: PermissionsListResponseSchema,
            400: ErrorResponseSchema,
            500: ErrorResponseSchema,
        }
    )
    def list_permissions(self):
        """List all possible permissions"""
        # 1. Get all permissions
        permissions_list_result: Result[List[PermissionEntity]] = self.authz_orchestration.list_permissions()
        # 2. parse result
        return Result.result_parser(
            result=permissions_list_result,
            ok_handler= lambda ok_value : (200, PermissionsListResponseSchema(permissions=ok_value)),
        )


    @route.get(
        '/users/{user_id}/roles',
        tags=['authz'],
        auth=JWTAuth(),
        permissions=None,
        response={
            200: ListRolesResponseSchema,
            400: ErrorResponseSchema,
            500: ErrorResponseSchema,
        }
    )
    def get_user_roles(self, user_id: UUID):
        # 1. Get user's roles
        user_roles_result: Result[List[RoleEntity]] = self.authz_orchestration.get_user_roles(user_id)

        return Result.result_parser(
            result=user_roles_result,
            ok_handler=lambda ok_value: (200, ListRolesResponseSchema(roles=ok_value)),
            default_error_message="internal server error",
        )

    @route.get(
        '/users/{user_id}/permissions',
        auth=JWTAuth(),
        permissions=None,
        response={
            200: PermissionsListResponseSchema,
            400: ErrorResponseSchema,
            500: ErrorResponseSchema,
        }
    )
    def get_user_permissions(self, user_id: UUID):
        """Return all permissions a user has (aggregated)"""
        user_permmissions_result: Result[List[PermissionEntity]] = self.authz_orchestration.get_user_permissions(user_id)
        return Result.result_parser(
            result=user_permmissions_result,
            ok_handler=lambda ok_value: (200, PermissionsListResponseSchema(permissions=ok_value)),
            default_error_message="internal server error",
        )


    @route.get(
        'users/{user_id}/can/{action}',
        tags=['authz'],
        auth=JWTAuth(),
        permissions=None,
        response={
            200: CanPermissionResponseSchema,
            400: ErrorResponseSchema,
            500: ErrorResponseSchema,
        }
    )
    def can_user(self, user_id:UUID, action: str):
        # 1. 
        user_can_result: Result[CanPermissionResponseVo] = self.authz_orchestration.can_user(
            user_id = user_id,
            action = action,
        )

        return Result.result_parser(
            result=user_can_result,
            ok_handler=lambda vo: (200, CanPermissionResponseSchema(
                user_id=vo.user_id,
                action=vo.action,
                authorized=vo.authorized
            )),
        )


    @route.get(
        '/roles/{role_id}/permissions',
        tags=['authz'],
        auth=JWTAuth(),
        permissions=None,
        response={
            200: PermissionsListResponseSchema,
            400: ErrorResponseSchema,
            500: ErrorResponseSchema,
        }
    )
    def get_role_permissions(self, role_id: UUID):
        """Get permissions assigned to a role"""
        role_permmisions_result: Result[List[PermissionEntity]] = self.authz_orchestration.get_role_permissions(role_id)
        return Result.result_parser(
            result=role_permmisions_result,
            ok_handler=lambda ok_value: (200, PermissionsListResponseSchema(permissions=ok_value)),
            default_error_message="internal server error",
        )

    @route.post(
        '/roles/{role_id}/permissions',
        tags=['authz'],
        permissions=None,
        auth=JWTAuth(),
        response={
            200: AssignPermissionToRoleResponseSchema,
            400: ErrorResponseSchema,
            500: ErrorResponseSchema,
        }
    )
    def assign_permission_to_role(self, request: AssignPermissionToRoleRequestSchema):
        """
        Assign a permission to a role (admin only)
        """
        assignment_result: Result = self.authz_orchestration.assign_permission_to_role(
            role_id=request.role_id,
            permission_slug=request.permission_slug
        )

        return Result.result_parser(
            result=assignment_result,
            ok_handler=lambda role_id, permisison_slug, is_success, : (201, AssignPermissionToRoleResponseSchema(
                is_sucessful=is_success,
                role_id=role_id,
                permission_slug=permisison_slug
            )),
            default_error_message="internal server error",
        )

    @route.delete(
        'roles/{role_id}/permissions',
        tags=['authz'],
        permissions=None,
        auth=JWTAuth(),
        response={
            200: RemovePermissionToRoleResponseSchema,
            400: ErrorResponseSchema,
            500: ErrorResponseSchema,
        }
    )
    def remove_permission_from_role(self, request: RemovePermissionToRoleRequestSchema):
        """
        Remove a permission from a role (admin only)
        """
        remove_permission_result: Result = self.authz_orchestration.remove_permission_from_role(
            role_id=request.role_id,
            permission_slug=request.permission_slug
        )
        return Result.result_parser(
            result=remove_permission_result,
            ok_handler=lambda role_id, permisison_slug, is_success: (204, RemovePermissionToRoleResponseSchema(
                is_sucessful=is_success,
                role_id=role_id,
                permission_slug=permisison_slug
            )),
            default_error_message="internal server error",
        )



    @route.delete(
        '/users/{user_id}/roles/{role_id}',
        tags=['authz'],
        permissions=None,
        auth=JWTAuth(),
        response={
            204: None,
            400: ErrorResponseSchema,
            500: ErrorResponseSchema,
        }
    )
    def remove_role_from_user(self, user_id: UUID, role_id: UUID):
        """
        Remove a role from a user (admin only)
        """
        remove_role_result: Result = self.authz_orchestration.remove_role_from_user(
            user_id=user_id,
            role_id=role_id
        )
        return Result.result_parser(
            result=remove_role_result,
            ok_handler=lambda user_id, role_id, is_success: (204, None),
            default_error_message="internal server error",
        )