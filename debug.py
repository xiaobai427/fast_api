# from pymongo import MongoClient
#
#
# def update_roles():
#     # 连接到MongoDB
#     client = MongoClient('localhost', 27017)
#     db = client['test_data']  # 更改为您的数据库名称
#
#     # 自动获取所有集合
#     collections = db.list_collection_names()
#     for collection_name in collections:
#         print(f"Updating collection: {collection_name}")
#         collection = db[collection_name]
#         roles = collection.find()
#
#         for index, role in enumerate(roles):
#             # 更新文档的 'id' 字段
#             collection.update_one(
#                 {'_id': role['_id']},
#                 {'$set': {'id': index}}  # 将 'id' 设置为索引值
#             )
#
#
# if __name__ == "__main__":
#     update_roles()

# from pymongo import MongoClient
# from datetime import datetime
# from bson.objectid import ObjectId  # 导入ObjectId
#
#
# #
# #
# def update_roles():
#     # 连接到MongoDB
#     client = MongoClient('localhost', 27017)
#     db = client['wbsite']  # 更改为您的数据库名称
#
#     # 获取所有文档
#     roles = roles_collection.find()
#
#     for index, role in enumerate(roles):
#         # 解析字符串格式的时间
#         # create_time = datetime.strptime(role['create_time'], "%Y-%m-%d %H:%M:%S")
#         # update_time = datetime.strptime(role['update_time'], "%Y-%m-%d %H:%M:%S")
#
#         # 将is_deleted从int转换为bool（这里的原代码已经是bool类型了，所以这一步可能是个误会或不需要的）
#         is_deleted = role['is_deleted']
#
#         # 更新文档
#         roles_collection.update_one(
#             {'_id': role['_id']},
#             {'$set': {
#                 'id': int(index),  # 更新id为新的ObjectId
#             }}
#         )
#
#
# if __name__ == "__main__":
#     update_roles()
import asyncio

# from mongoengine import connect, disconnect
# from pymongo import MongoClient
# import mysql.connector
#
#
# # MongoDB操作：列出数据库、集合、第一个文档的字段及其类型
# def mongo_operations():
#     print("MongoDB操作:")
#     connect(host='mongodb://localhost:27017/')
#     client = MongoClient('localhost', 27017)
#     db_names = client.list_database_names()
#     for db_name in db_names:
#         print(f"\n数据库: {db_name}")
#         db = client[db_name]
#         collection_names = db.list_collection_names()
#         for collection_name in collection_names:
#             print(f"  集合: {collection_name}")
#             collection = db[collection_name]
#             document = collection.find_one()
#             if document:
#                 print("    字段、值和类型:")
#                 for key, value in document.items():
#                     value_type = type(value).__name__  # 获取值的类型名称
#                     print(f"      {key}: {value} ({value_type})")
#             else:
#                 print("    集合是空的")
#     disconnect()
#
#
# # MySQL操作：列出数据库表、列及其属性
# def mysql_operations():
#     print("\nMySQL操作:")
#     cnx = mysql.connector.connect(user='root', password='123456',
#                                   host='127.0.0.1',
#                                   database='test_data')
#     cursor = cnx.cursor()
#     cursor.execute("SHOW TABLES;")
#     tables = cursor.fetchall()
#     for (table_name,) in tables:
#         print(f"\n表: {table_name}")
#         cursor.execute(f"DESCRIBE {table_name};")
#         columns = cursor.fetchall()
#         print("  列和属性:")
#         for column in columns:
#             print(
#                 f"    列名: {column[0]}, 类型: {column[1]}, Null允许: {column[2]}, 键: {column[3]}, 默认值: {column[4]}, 额外信息: {column[5]}")
#     cursor.close()
#     cnx.close()
#
#
# if __name__ == "__main__":
#     mongo_operations()
#
#
# from beanie import Document, init_beanie
# from motor.motor_asyncio import AsyncIOMotorClient
# from pydantic import Field
# from datetime import datetime
# from typing import Union
#
# from models import Spur, AntCalibCrossFreq, Calibration, Eirp, RoleTest, Pattern
#
#
# class RoleBaseDocument(Document):
#     role_name: str = Field(..., max_length=50)
#     role_code: str = Field(..., max_length=50)
#     description: str = Field(...)
#     create_time: Union[datetime, str] = Field(...)
#     update_time: Union[datetime, str] = Field(...)
#     is_deleted: bool = Field(default=False)  # 将 is_deleted 统一为布尔类型
#
#     class Settings:
#         arbitrary_types_allowed = True
#         orm_mode = True
#
#
# class RoleWbsite(RoleBaseDocument):
#     id: Union[int, str] = Field(..., primary_field=True, alias='id')
#
#     class Settings:
#         name = "roles"
#         database = "wbsite"
#
#
# async def main():
#     # 初始化数据库连接
#     client_test_data = AsyncIOMotorClient("mongodb://localhost:27017/test_data")
#     client_wbsite = AsyncIOMotorClient("mongodb://localhost:27017/wbsite")
#
#     # 对每个数据库进行Beanie初始化
#     await init_beanie(database=client_test_data.test_data,
#                       document_models=[Spur, AntCalibCrossFreq, Calibration, Eirp, Pattern, RoleTest])
#     await init_beanie(database=client_wbsite.wbsite, document_models=[RoleWbsite])
#
#     # 更新文档
#     # async for role in Calibration.find():
#     #     if isinstance(role.create_time, str):
#     #         role.create_time = datetime.strptime(role.create_time, "%d/%m/%Y %H:%M:%S")
#     #     if isinstance(role.update_time, str):
#     #         role.update_time = datetime.strptime(role.update_time, "%d/%m/%Y %H:%M:%S")
#     #     role.is_deleted = bool(int(role.is_deleted))  # 从整型转换为布尔型
#     #     await role.save()
#
#     # 查询并打印更新后的文档
#     print("\nUpdated Documents:")
#     async for role in Calibration.find():
#         print(role)
#         # print(f"ID: {role.id}, Role Name: {role.role_name}, Create Time: {role.create_time}, "
#         #       f"Update Time: {role.update_time}, Is Deleted: {role.is_deleted}")
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
#     # print(uuid.uuid4().hex)

from datetime import datetime
from pydantic import BaseModel, Field

from typing import List, Optional, Union, Type
from beanie import PydanticObjectId, Document

from log_manager import log_manager
from models import RoleWbsite
from services.base import BaseDatabaseOperations


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
    create_time: datetime
    update_time: datetime = Field(default_factory=datetime.now)
    is_deleted: bool


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


class RoleDatabaseOperations(BaseDatabaseOperations[RoleCreateRequest, RoleResponse]):
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
        roles = await RoleWbsite.find_all().to_list()

        for role in roles:
            log_manager.debug(f"Role: {role}")

        return [RoleResponse(**role.dict()) for role in
                roles]

    async def search(self, name: Optional[str] = None, code: Optional[str] = None) -> List[RoleResponse]:
        query = {}
        if name:
            query["role_name"] = {"$regex": name, "$options": "i"}
        if code:
            query["role_code"] = {"$regex": code, "$options": "i"}
        roles = await RoleWbsite.find(query).to_list()
        return [RoleResponse(**role.dict()) for role in
                roles]

    async def get_by_id(self, record_id: Union[int, str, PydanticObjectId]) -> RoleResponse:
        role = await RoleWbsite.get(record_id)
        return RoleResponse(**role.dict())

    async def update(self, record_id: Union[PydanticObjectId, int, str],
                     update_data: RoleCreateRequest) -> RoleResponse:
        role = await RoleWbsite.get(record_id)
        role.role_name = update_data.role_name
        role.role_code = update_data.role_code
        role.description = update_data.description
        await role.save()
        return RoleResponse(**role.dict())

    async def delete(self, record_id: PydanticObjectId) -> None:
        role = await RoleWbsite.get(record_id)
        await role.delete()


#
#
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from models import RoleWbsite, RoleTest
from services.role_batabase import RoleTestDatabaseOperations, RoleWbsiteDatabaseOperations


async def init_db():
    # 连接到数据库
    client_test_data = AsyncIOMotorClient("mongodb://localhost:27017/test_data")
    client_wbsite = AsyncIOMotorClient("mongodb://localhost:27017/wbsite")

    # 初始化Beanie，指定文档模型和数据库
    await init_beanie(database=client_test_data.get_database("test_data"), document_models=[RoleTest])
    await init_beanie(database=client_wbsite.get_database("wbsite"), document_models=[RoleWbsite])


# async def run_tests():
#     await init_db()  # 确保先初始化数据库
#
#     role_wbsite_ops = RoleDatabaseOperations()
#
# #     print(role_wbsite_ops)
# # #
# # #     # 获取所有角色
# #     roles = await role_wbsite_ops.get_all()
# #
# #     roles = await role_wbsite_ops.create()
# #     print("Roles:", roles)
# #
# #
# if __name__ == "__main__":
#     asyncio.run(run_tests())

async def run_tests():
    await init_db()  # 确保先初始化数据库

    # 创建 RoleDatabaseOperations 实例
    role_wbsite_ops = RoleDatabaseOperations()

    # 创建新角色的数据
    new_role_data = RoleCreateRequest(
        role_name="Example Role",
        role_code="example_code",
        description="This is an example role description."
    )

    # 创建新角色
    new_role = await role_wbsite_ops.create(new_role_data)
    print("New Role Created:", new_role)


if __name__ == "__main__":
    asyncio.run(run_tests())

# import asyncio
# from motor.motor_asyncio import AsyncIOMotorClient
#
#
# async def copy_collection(source_db_name, target_db_name, collection_name):
#     # 创建MongoDB异步客户端实例
#     client = AsyncIOMotorClient("mongodb://localhost:27017")
#
#     # 获取源数据库和目标数据库的引用
#     source_db = client[source_db_name]
#     target_db = client[target_db_name]
#
#     # 获取集合的引用
#     source_collection = source_db[collection_name]
#     target_collection = target_db[collection_name]
#
#     # 读取源集合中的所有文档
#     documents = await source_collection.find().to_list(length=None)
#
#     # 如果目标集合中有数据，先清空目标集合
#     await target_collection.delete_many({})
#
#     # 如果源集合中有文档，复制到目标集合
#     if documents:
#         await target_collection.insert_many(documents)
#
#     print(
#         f"Successfully copied {len(documents)} documents from {source_db_name}.{collection_name} to {target_db_name}.{collection_name}")
#
#
# # 初始化和运行异步操作
# asyncio.run(copy_collection("wbsite", "test_data", "roles"))
