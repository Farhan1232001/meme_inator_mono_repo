/// Authorization Endpoints (RBAC)
class AuthorizationEndpoints {
  // Roles
  static const String listRoles = '/authz/roles';
  
  // Permissions
  static const String listPermissions = '/authz/permissions';
  
  // User roles & permissions
  static const String getUserRoles = '/authz/users/{user_id}/roles';
  static const String getUserPermissions = '/authz/users/{user_id}/permissions';
  static const String checkUserPermission = '/authz/users/{user_id}/can/{action}';
  
  // Role permissions management
  static const String getRolePermissions = '/authz/roles/{role_id}/permissions';
  static const String assignPermissionToRole = '/authz/roles/{role_id}/permissions';
  static const String removePermissionFromRole = '/authz/roles/{role_id}/permissions';
  
  // Path parameter helpers
  static String userRoles(String userId) => '/authz/users/$userId/roles';
  static String userPermissions(String userId) => '/authz/users/$userId/permissions';
  static String canUserPerform(String userId, String action) => '/authz/users/$userId/can/$action';
  static String rolePermissions(String roleId) => '/authz/roles/$roleId/permissions';
}
