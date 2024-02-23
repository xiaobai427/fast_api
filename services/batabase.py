from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# 基础文档请求模型
class BaseDocumentRequest(BaseModel):
    type: str
    board_name: str
    data: Optional[str] = None
    started_at: Optional[datetime] = None
    stopped_at: Optional[datetime] = None
    tester: Optional[str] = None
    chip_name: Optional[str] = None
    chip_rev: Optional[str] = None
    board_rev: Optional[str] = None
    sn: Optional[str] = None
    comment: Optional[str] = None
    is_deleted: Optional[bool] = False
    darkroom: Optional[str] = None
    status: Optional[str] = None
    fail_reason: Optional[str] = None


# 基础文档响应模型
class BaseDocumentResponse(BaseModel):
    id: int
    type: str
    board_name: str
    data: Optional[str]
    started_at: Optional[datetime]
    stopped_at: Optional[datetime]
    tester: Optional[str]
    chip_name: Optional[str]
    chip_rev: Optional[str]
    board_rev: Optional[str]
    sn: Optional[str]
    comment: Optional[str]
    is_deleted: bool
    darkroom: Optional[str]
    status: Optional[str]
    fail_reason: Optional[str]

    class Config:
        orm_mode = True


# class SpurRequest(BaseDocumentRequest):
#     extra_field: Optional[str] = None
#
#
# class SpurResponse(BaseDocumentResponse):
#     extra_field: Optional[str]
#
#     class Config:
#         orm_mode = True
