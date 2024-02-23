# api/base.py
from typing import Union, Optional, TypeVar, Generic, Type

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException
from common.result import Result, ResultCode
from log_manager import log_manager
from services.role_batabase import RoleCreateRequest, RoleDatabaseOperationsBase


router = APIRouter()

# 定义一个类型变量

T = TypeVar("T", bound=RoleDatabaseOperationsBase)


class RoleAPIHandler(Generic[T]):
    def __init__(self, db_ops_cls: Type[T]):
        self.db_ops_cls = db_ops_cls()

    async def create_role(self, role_request: RoleCreateRequest):
        try:
            role = await self.db_ops_cls.create(role_request)
            return Result.success(role)
        except Exception as e:
            log_manager.error(f"Error creating role: {e}")
            # 这里假设所有异常都是服务错误，你可能需要根据异常的类型来调整错误码
            return HTTPException(ResultCode.SERVICE_ERROR.value, str(e))

    async def list_roles(self):
        try:
            roles = await self.db_ops_cls.get_all()
            return Result.success(roles)
        except Exception as e:
            log_manager.error(f"Error listing roles: {e}")
            return HTTPException(ResultCode.SERVICE_ERROR.value, str(e))

    async def get_role(self, role_id: Union[int, str, PydanticObjectId]):
        try:
            role = await self.db_ops_cls.get_by_id(role_id)
            if role is None:
                return Result.fail(f"Role with ID {role_id} not found")
            return Result.success(role)
        except Exception as e:
            log_manager.error(f"Error getting role: {e}")
            return HTTPException(ResultCode.SERVICE_ERROR.value, str(e))

    async def search_roles(self, id_: Union[str, int], role_name: Optional[str], role_code: Optional[str]):
        try:
            roles = await self.db_ops_cls.search(id_, role_name, role_code)
            return Result.success(roles)
        except Exception as e:
            log_manager.error(f"Error searching roles: {e}")
            return HTTPException(ResultCode.SERVICE_ERROR.value, str(e))

    async def update_role(self, role_id: Union[str, int], role_request: RoleCreateRequest):
        try:
            updated_role = await self.db_ops_cls.update(role_id, role_request)
            if updated_role is None:
                return Result.fail(f"Role with ID {role_id} not found")
            return Result.success(updated_role)
        except Exception as e:
            log_manager.error(f"Error updating role: {e}")
            return HTTPException(ResultCode.SERVICE_ERROR.value, str(e))

    async def delete_role(self, role_id: Union[str, int]):
        try:
            deleted_role = await self.db_ops_cls.delete(role_id)
            if deleted_role is None:
                return Result.fail(f"Role with ID {role_id} not found")
            return Result.success(deleted_role)
        except Exception as e:
            log_manager.error(f"Error deleting role: {e}")
            return HTTPException(ResultCode.SERVICE_ERROR.value, str(e))