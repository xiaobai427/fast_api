from pydantic import BaseModel, Field
from enum import Enum
from typing import Generic, TypeVar, Optional

T = TypeVar('T')


class ResultCode(Enum):
    SUCCESS = 200
    FAIL = 400
    SERVICE_ERROR = 500
    DATA_ERROR = 422
    LOGIN_AUTH = 401
    PERMISSION = 403


# 让Result类继承自BaseModel，并使用泛型
class Result(BaseModel, Generic[T]):
    code: ResultCode
    message: str
    data: Optional[T] = None

    @classmethod
    def build(cls, code: ResultCode, message: str, data: Optional[T] = None) -> "Result":
        return cls(code=code, message=message, data=data)

    @classmethod
    def success(cls, data: Optional[T] = None) -> "Result[T]":
        return cls.build(ResultCode.SUCCESS, "成功", data)

    @classmethod
    def fail(cls, message: str = "失败", data: Optional[T] = None) -> "Result[T]":
        return cls.build(ResultCode.FAIL, message, data)

