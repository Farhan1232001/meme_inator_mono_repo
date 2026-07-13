from pydantic import BaseModel


class VisibilitySchema(BaseModel):
    is_online: bool
