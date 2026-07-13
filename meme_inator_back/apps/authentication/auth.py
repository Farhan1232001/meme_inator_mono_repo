from ninja_jwt.authentication import JWTAuth
from django.http import HttpRequest

# Assume you have a request object
# request = HttpRequest()
# request.headers['Authorization'] = 'Bearer <your_actual_jwt_token>'time
def jwt_authenticator(request: HttpRequest):
    authenticator = JWTAuth()

    # Call the authenticate method
    # It returns a user object if valid, or None/raises an exception if invalid
    user = authenticator.authenticate(request, **{})

    if user:
        print(f"User {user.username} is authenticated!")
        # You can now proceed with your logic
        return user
    else:
        print("Authentication failed.")
        # Handle the unauthenticated case (e.g., return a 401 response)
        return None