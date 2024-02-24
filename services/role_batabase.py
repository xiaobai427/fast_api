from datetime import datetime
from pydantic import BaseModel, Field

from typing import List, Optional, Union, Type, TypeVar, Generic
from beanie import Document

from models import RoleWbsite, RoleTest
from services.base import BaseDatabaseOperations

# 定义一个类型变量，用于泛型
T = TypeVar('T', bound=Document)


# 假设的Pydantic请求和响应模型
class RoleCreateRequest(BaseModel):
    role_name: str
    role_code: str
    description: Optional[str] = None


class RoleResponse(BaseModel):
    id: int
    role_name: str
    role_code: str
    description: Optional[str]
    create_time: Union[datetime, str] = Field(default_factory=datetime.now)
    update_time: Union[datetime, str] = Field(default_factory=datetime.now)
    is_deleted: bool = Field(default=False)


async def get_next_sequence(model: Type[Document]) -> int:
    # Use the model's class name as a unique identifier for the counter
    sequence_name = model.Settings.name
    # Access the database client from the model's associated collection
    db = model.get_motor_collection().database
    # Access the 'counters' collection from the same database
    counters_collection = db.get_collection('counters')

    result = await counters_collection.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=True
    )
    return result["sequence_value"]


class RoleDatabaseOperationsBase(Generic[T], BaseDatabaseOperations[RoleCreateRequest, RoleResponse]):
    model: Type[T]  # 指定模型类型

    async def create(self, create_data: RoleCreateRequest) -> RoleResponse:
        new_id = await get_next_sequence(RoleWbsite)  # Generate the next ID
        role = RoleWbsite(
                          id=new_id,
                          role_name=create_data.role_name,
                          role_code=create_data.role_code,
                          description=create_data.description)
        role_dict = role.dict()
        await role.get_motor_collection().insert_one(role_dict)
        return RoleResponse(**role.dict())

    async def get_all(self) -> List[RoleResponse]:
        roles = await self.model.find_all().to_list()
        return [RoleResponse(**role.dict()) for role in roles]

    async def search(self,
                     id_: Optional[str] = None,
                     name: Optional[str] = None,
                     code: Optional[str] = None) -> List[RoleResponse]:
        # 构建查询条件，只包含非None的参数
        query = {
            **({"id": {"$regex": id_, "$options": "i"}} if id_ else {}),
            **({"role_name": {"$regex": name, "$options": "i"}} if name else {}),
            **({"role_code": {"$regex": code, "$options": "i"}} if code else {})
        }
        roles = await self.model.find(query).to_list()
        return [RoleResponse(**role.dict()) for role in roles]

    async def get_by_id(self, record_id: Union[int, str]) -> RoleResponse:
        role = await self.model.get(record_id)
        return RoleResponse(**role.dict())

    async def update(self, record_id: Union[int, str],
                     update_data: RoleCreateRequest) -> RoleResponse:
        role = await self.model.get(record_id)
        role.role_name = update_data.role_name
        role.role_code = update_data.role_code
        role.description = update_data.description
        await role.save()
        return RoleResponse(**role.dict())

    async def delete(self, record_id: Union[int, str]) -> None:
        role = await self.model.get(record_id)
        await role.delete()


class RoleTestDatabaseOperations(RoleDatabaseOperationsBase[RoleTest]):
    model = RoleTest


class RoleWbsiteDatabaseOperations(RoleDatabaseOperationsBase[RoleWbsite]):
    model = RoleWbsite
