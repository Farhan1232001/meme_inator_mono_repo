from pydantic import BaseModel

class ChangeUsernameSchema(BaseModel):
    new_username: str
