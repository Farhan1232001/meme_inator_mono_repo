# from ninja_extra.security import HttpBearer
# from django.http import HttpRequest
# from typing import Optional
# from typing import Optional
# from ninja_jwt.authentication import JWTAuth
# from meme_inator_back import settings
# from core.dependency_injections import di
# from ninja_jwt.exceptions import AuthenticationFailed
# from django.contrib.auth.models import AnonymousUser

# class OptionalJWTAuth(HttpBearer):
#     """
#     Authentication that optionally validates JWT token.
#     Returns user if token is valid, AnonymousUser if no token, 
#     raises AuthenticationFailed if invalid token.
#     """
    
#     def authenticate(self, request: HttpRequest, token: Optional[str] = None):
#         # If no token is provided, return AnonymousUser
#         if not token:
#             return AnonymousUser()
        
#         try:
#             # Validate token
#             jwt_auth = JWTAuth()
#             user = jwt_auth.authenticate(request, token)
#             return user
#         except AuthenticationFailed:
#             # If token is provided but invalid, raise exception
#             raise AuthenticationFailed("Invalid token")
#         except Exception as e:
#             # Log unexpected errors
#             print(f"Unexpected auth error: {e}")
#             raise AuthenticationFailed("Authentication failed")

