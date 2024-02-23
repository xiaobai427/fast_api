from beanie import Document
from pydantic import Field
from typing import Union
from datetime import datetime


class RoleBaseDocument(Document):
    role_name: str = Field(..., max_length=50)
    role_code: str = Field(..., max_length=50)
    description: str = Field(...)
    create_time: Union[datetime, str] = Field(default_factory=datetime.now)
    update_time: Union[datetime, str] = Field(default_factory=datetime.now)
    is_deleted: bool = Field(default=False)

    class Settings:
        arbitrary_types_allowed = True
        orm_mode = True
        # 启用状态管理
        state_management = True


class BaseDocument(Document):
    type: str = Field(...)
    board_name: str = Field(...)
    data: str = Field(...)
    started_at: datetime = Field(...)
    stopped_at: datetime = Field(...)
    tester: str = Field(...)
    chip_name: str = Field(...)
    chip_rev: str = Field(...)
    board_rev: str = Field(...)
    sn: str = Field(...)
    comment: str = Field(...)
    is_deleted: bool = Field(default=False)
    darkroom: str = Field(...)
    status: str = Field(...)
    fail_reason: str = Field(...)

    class Settings:
        arbitrary_types_allowed = True
        orm_mode = True
