from datetime import timedelta

JWT_SECRET = "replace-with-your-secret-from-env"  # use env var in production
JWT_ALGORITHM = "HS256"

ACCESS_TOKEN_LIFETIME = timedelta(minutes=15)
REFRESH_TOKEN_LIFETIME = timedelta(days=7)
