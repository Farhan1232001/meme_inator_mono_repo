from pydantic import BaseModel


class UnreadCountSchema(BaseModel):
    unread_count: int

    class Config:
        json_schema_extra = {"example": {"unread_count": 5}}


