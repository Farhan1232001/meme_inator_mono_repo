from pydantic import BaseModel, Field

class ChangePasswordSchema(BaseModel):
    current_password: str = Field(..., description="The user's current password")
    new_password: str = Field(..., description="The new password to set")
