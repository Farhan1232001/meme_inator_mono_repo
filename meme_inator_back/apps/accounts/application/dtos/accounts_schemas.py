# apps/accounts/application/dtos/accounts_schemas.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional


# -------------------------
# Password change (auth)
# -------------------------
class PasswordChangeRequestSchema(BaseModel):
    current_password: str = Field(..., description="Current password of the user")
    new_password: str = Field(..., description="New password to set")


class PasswordChangeResponseSchema(BaseModel):
    success: bool = Field(..., example=True)
    message: Optional[str] = Field(None, example="Password updated")


# -------------------------
# Password reset (intent)
# -------------------------
class PasswordResetIntentRequestSchema(BaseModel):
    email: EmailStr = Field(..., description="Registered email to send reset challenge to")


class PasswordResetIntentResponseSchema(BaseModel):
    success: bool = Field(..., example=True)
    message: Optional[str] = Field(None, example="Reset challenge sent")


# -------------------------
# Password reset (confirm)
# -------------------------
class PasswordResetConfirmRequestSchema(BaseModel):
    challenge_code: str = Field(..., description="Challenge code sent via email")
    new_password: str = Field(..., description="New password to set")


class PasswordResetConfirmResponseSchema(BaseModel):
    success: bool = Field(..., example=True)
    message: Optional[str] = Field(None, example="Password reset successful")


# -------------------------
# Email change (intent)
# -------------------------
class EmailChangeIntentRequestSchema(BaseModel):
    new_email: EmailStr = Field(..., description="New email to verify")


class EmailChangeIntentResponseSchema(BaseModel):
    success: bool = Field(..., example=True)
    message: Optional[str] = Field(None, example="Verification challenge sent")


# -------------------------
# Email change (confirm)
# -------------------------
class EmailChangeConfirmRequestSchema(BaseModel):
    challenge_code: str = Field(..., description="Challenge code sent to the new email")


class EmailChangeConfirmResponseSchema(BaseModel):
    success: bool = Field(..., example=True)
    message: Optional[str] = Field(None, example="Email updated")
