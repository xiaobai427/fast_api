from enum import Enum
from fastapi import HTTPException
from typing import Generic, TypeVar, Optional

T = TypeVar('T')


class ResultCode(Enum):
    SUCCESS = 200
    FAIL = 400
    SERVICE_ERROR = 500
    DATA_ERROR = 422
    LOGIN_AUTH = 401
    PERMISSION = 403


class Result(Generic[T]):
    code: ResultCode
    message: str
    data: Optional[T] = None

    @classmethod
    def build(cls, code: ResultCode, message: str, data: T = None) -> dict:
        return {
            "code": code.value,
            "message": message,
            "data": data
        }

    @classmethod
    def ok(cls, data: T = None) -> dict:
        return cls.build(ResultCode.SUCCESS, "成功", data)

    @classmethod
    def fail(cls, message: str = "失败", data: T = None) -> dict:
        return cls.build(ResultCode.FAIL, message, data)

    # 用于处理需要抛出异常的情况
    @staticmethod
    def error(status_code: int, detail: str):
        raise HTTPException(status_code=status_code, detail=detail)
