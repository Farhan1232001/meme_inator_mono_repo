from dataclasses import dataclass
from typing import Generic, TypeVar, Optional, Any

T = TypeVar("T")

class Result:
    @staticmethod
    def result_parser(
        *,
        result: Result,
        ok_handler,
        default_error_message: str = "internal server error",
    ):
        from meme_inator_back import settings  # local import to avoid circular import

        match result:
            case Ok(value=value):
                return ok_handler(value)

            case NotOk(message=message, static_msg=static_msg, status_code=status_code):
                return status_code, {
                    "message": message,
                    "static_msg": static_msg,
                }

            case Error(message=message, static_msg=static_msg, exception=exception, status_code=status_code):
                if settings.DEBUG:
                    return status_code, {
                        "message": message,
                        "static_msg": static_msg,
                        "exception_str": str(exception) if exception else None,
                    }
                return status_code, {
                    "message": default_error_message,
                    "static_msg": static_msg,
                }

            case _:
                return 500, {
                    "message": default_error_message,
                    "static_msg": "UNEXPECTED_RESULT",
                }
    

    def is_ok(self) -> bool:
        """Returns True if this is an Ok result"""
        return isinstance(self, Ok)
    
    def is_not_ok(self) -> bool:
        """Returns True if this is a NotOk result"""
        return isinstance(self, NotOk)
    
    def is_error(self) -> bool:
        """Returns True if this is an Error result"""
        return isinstance(self, Error)

@dataclass
class Ok(Result, Generic[T]):
    value: T

@dataclass
class NotOk(Result):
    message: str
    static_msg: Optional[str] = None   # optional machine code, e.g. "USERNAME_TAKEN"
    status_code: int = 400       # default HTTP status suggestion

@dataclass
class Error(Result):
    message: str = "internal server error"
    static_msg: str = 'null'
    exception: Optional[Exception] = None
    status_code: int = 500      # default HTTP status suggestion
