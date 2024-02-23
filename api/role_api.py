# api/role_api.py
import logging
from typing import Union, Optional
from fastapi import Query

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends
from common.result import Result
from services.role_batabase import RoleWbsiteDatabaseOperations, RoleCreateRequest

logger = logging.getLogger(__name__)

router = APIRouter()


# 依赖注入的方式获取数据库操作实例
def get_role_db_ops() -> RoleWbsiteDatabaseOperations:
    return RoleWbsiteDatabaseOperations()


@router.get("/roles/search", response_model=dict)
async def search_roles(role_name: Optional[str] = Query(None), role_code: Optional[str] = Query(None), db_ops: RoleWbsiteDatabaseOperations = Depends(get_role_db_ops)):
    try:
        roles = await db_ops.search(name=role_name, code=role_code)
        return Result.ok(roles)
    except Exception as e:
        logger.error(f"Error searching roles: {e}")
        return Result.fail(str(e))


@router.post("/roles/", response_model=dict)
async def create_role(role_request: RoleCreateRequest, db_ops: RoleWbsiteDatabaseOperations = Depends(get_role_db_ops)):
    try:
        role = await db_ops.create(role_request)
        return Result.ok(role)
    except Exception as e:
        return Result.fail(str(e))


@router.get("/roles/", response_model=dict)
async def list_roles(db_ops: RoleWbsiteDatabaseOperations = Depends(get_role_db_ops)):
    try:
        roles = await db_ops.get_all()
        return Result.ok(roles)
    except Exception as e:
        return Result.fail(str(e))


@router.get("/roles/{role_id}", response_model=dict)
async def get_role(role_id: Union[int, str, PydanticObjectId], db_ops: RoleWbsiteDatabaseOperations = Depends(get_role_db_ops)):
    try:
        role = await db_ops.get_by_id(role_id)
        return Result.ok(role)
    except Exception as e:
        return Result.fail(str(e))


@router.put("/roles/{role_id}", response_model=dict)
async def update_role(role_id: Union[int, str, PydanticObjectId], role_request: RoleCreateRequest,
                      db_ops: RoleWbsiteDatabaseOperations = Depends(get_role_db_ops)):
    try:
        updated_role = await db_ops.update(role_id, role_request)
        return Result.ok(updated_role)
    except Exception as e:
        return Result.fail(str(e))


@router.delete("/roles/{role_id}", response_model=dict)
async def delete_role(role_id: PydanticObjectId, db_ops: RoleWbsiteDatabaseOperations = Depends(get_role_db_ops)):
    try:
        await db_ops.delete(role_id)
        return Result.ok({"message": "Role deleted successfully"})
    except Exception as e:
        return Result.fail(str(e))
