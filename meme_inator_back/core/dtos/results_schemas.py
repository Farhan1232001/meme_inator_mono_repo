from typing import Optional
from ninja import Schema

# Contains GENERIC Result schemas. 

# Generic OkResponseSchema not needed

class NotOkResponseSchema(Schema):
    message: str
    static_msg: Optional[str] = None

class ErrorResponseSchema(Schema):
    message: str
    static_msg: Optional[str] = None  # machine-readable error code
    exception_str: Optional[str] = None  # only for debug