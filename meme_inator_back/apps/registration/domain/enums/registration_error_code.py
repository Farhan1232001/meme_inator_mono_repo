# apps/registration/domain/errors.py
from enum import Enum

class RegistrationErrorCode(str, Enum):
    USERNAME_TAKEN = "USERNAME_TAKEN"
    EMAIL_TAKEN = "EMAIL_TAKEN"
    PASSWORD_TOO_WEAK = "PASSWORD_TOO_WEAK"
