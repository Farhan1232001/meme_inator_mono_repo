from tokenize import TokenError

from ninja import Schema
from ninja_extra import api_controller, http_post
from django.contrib.auth import authenticate
from apps.users.models import UserModel
from ninja_jwt.tokens import RefreshToken, Token
from ninja_jwt.authentication import JWTAuth
from django.http import HttpRequest

from meme_inator_back import settings

class TokenObtainScheme(Schema):
    """
    usecase: Logging In request schema
    """
    usernameOrEmail: str
    password: str
    remember_me: bool = False
    
class TokenRefreshSchema(Schema):
    """
    usecase: Logging Out request schema
    usecase: Refresh jwt token Request 
    """
    refresh: str

class TokenPairSchema(Schema):
    """
    usecase: Logging In Response schema
    usecase: Refresh JWT token Reponse
    """
    access: str
    refresh: str


# Constants
# TODO: put these in a constants.py file
TOKEN_PURPOSE_CLAIM = 'purpose'
PURPOSE_SESSION = 'session'
PURPOSE_PERSISTENT = 'persistent'
    

@api_controller('/auth', tags=['authentication'])
class AuthenticationController:

    # -- LOGIN -------------------------------------------------------------
    @http_post("/login", 
               response={200: TokenPairSchema, 401: str}, 
               auth=None
    )
    def login(self, 
              request: HttpRequest, 
              payload: TokenObtainScheme
        ):
        usernameOrEmail = payload.usernameOrEmail
        password = payload.password
        remember_me = payload.remember_me 
        
        # if authenticated, return user, otherwise None
        user = authenticate(request, username=usernameOrEmail, password=password)
        
        # case 1: IF usernameOrEmail IS email
        if user is None and '@' in usernameOrEmail:
            user = self._auth_user_by_email(request, usernameOrEmail, password)
            if user is None:
                return 401, "Invalid Credentials"
        
        elif user:
            # Generate refresh and access tokens with appropriate lifetimes
            return self._generate_refresh_and_access_tokens_for_user(user, remember_me)

        return 401, "Invalid credentials"

    # -- REFRESH TOKENS ------------------------------------------------------
    @http_post("/token/refresh", response={200: TokenPairSchema, 400: str}, auth=None)
    def refresh(self, request: HttpRequest, payload: TokenRefreshSchema):
        try:
            refresh = RefreshToken(payload.refresh)
            
            # Retrieve the purpose claim (default to 'session' if missing for backward compatibility)
            purpose = refresh.payload.get(TOKEN_PURPOSE_CLAIM, PURPOSE_SESSION)
            
            # Generate new access token (copies claims except those in no_copy_claims)
            new_access = refresh.access_token
            
            # Explicitly set the purpose claim on the new access token
            new_access[TOKEN_PURPOSE_CLAIM] = purpose
            
            # Adjust access token lifetime based on purpose
            if purpose == PURPOSE_PERSISTENT:
                new_access.set_exp(lifetime=settings.SIMPLE_JWT['REMEMBER_ME_ACCESS_TOKEN_LIFETIME'])
            else:
                # Use default access token lifetime (already set by access_token creation, but we can ensure it)
                new_access.set_exp(lifetime=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])
            
            # Return the same refresh token (if rotation is off) or a new one if you rotate
            return 200, {
                "access": str(new_access), 
                "refresh": str(refresh)   # unchanged unless you rotate
            }
        
        except TokenError as e:
            return 400, f"Token refresh failed: {e}"
        except Exception as e:
            return 400, f"Token refresh failed: {e}"
    
    # -- LOGOUT -------------------------------------------------------------
    @http_post('/logout',
               response={
                   200: dict,
                   400: dict
               },
               # logout doesnt need access token, refresh token is sufficient
               # this is ok though
               auth=JWTAuth() 
    )
    def logout(self, 
               request: HttpRequest, 
               payload: TokenRefreshSchema
        ):
        print('request', request)
        print('payload', payload)
        try:
            refresh = RefreshToken(payload.refresh)
            refresh.blacklist()
            
            return {
                'status_code': 200,
                'static_msg': 'LOGOUT_SUCCESS',
                'message': 'Logout successful.'
            }
        except Exception as e:
            return {
                'status_code': 400,
                'static_msg': 'LOGOUT_FAILED',
                'message': f'Logout failed. {e}' if settings.DEBUG else f'Logout failed.'
            }
 
 

    # -- UTILITY METHODS ----------------------------------------------------
    def _generate_refresh_and_access_tokens_for_user(self, user, remember_me: bool = False):
        refresh: RefreshToken = RefreshToken.for_user(user)
        
        # Determine token purpose
        purpose = PURPOSE_PERSISTENT if remember_me else PURPOSE_SESSION
        
        # Set custom claim
        refresh[TOKEN_PURPOSE_CLAIM] = purpose
        
        # Adjust lifetimes based on purpose
        if remember_me:
            refresh.set_exp(lifetime=settings.SIMPLE_JWT['REMEMBER_ME_REFRESH_TOKEN_LIFETIME'])
        else:
            refresh.set_exp(lifetime=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'])
        
        # Create access token from refresh (copies most claims, but we need to set purpose explicitly)
        access = refresh.access_token
        access[TOKEN_PURPOSE_CLAIM] = purpose
        
        # Set access token lifetime based on purpose
        if remember_me:
            access.set_exp(lifetime=settings.SIMPLE_JWT['REMEMBER_ME_ACCESS_TOKEN_LIFETIME'])
        # else: access token uses default lifetime (set by access_token creation)
        
        return 200, {
            "access": str(access), 
            "refresh": str(refresh)
        }
        
    
    def _auth_user_by_email(self, request, email, password) -> UserModel:
        """
        """
        # fun fact: emails are NOT case sensitive
        user = UserModel.objects.get(email__iexact=email)
        user = authenticate(
            request=request, 
            username=getattr(user, UserModel.USERNAME_FIELD),
            password = password
        )
        
        return user if user is not None else None

