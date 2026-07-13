# apps/authz/permissions.py
from ninja_extra import permissions
from ninja_jwt.authentication import JWTAuth

class IsProMemer(permissions.BasePermission):
    message = "You need ProMemer subscription to access this."

    # TODO: Should check if user from request is also actually logged in
    def has_permission(self, request, controller):
        authenticator = JWTAuth()
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        try:
            user_auth_tuple = authenticator.authenticate(request, token)
            if not user_auth_tuple:
                return False
            request.user = user_auth_tuple[0]
        except Exception:
            return False

        # Django Ninja JWT sets request.user to an instance of your user model if the JWT is valid.
        # The middleware 'django.contrib.auth.middleware.AuthenticationMiddleware'
        # also causes HTTPRequest to have user attribute
        user = getattr(request, 'user', None)
        if not user or not hasattr(user, 'groups'):
            return False
        return user.groups.filter(name="ProMemer").exists()
        
