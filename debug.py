# from pymongo import MongoClient
# from datetime import datetime
# from bson.objectid import ObjectId  # 导入ObjectId
#
#
# def update_roles():
#     # 连接到MongoDB
#     client = MongoClient('localhost', 27017)
#     db = client['wbsite']  # 更改为您的数据库名称
#     roles_collection = db['roles']  # 假设集合名称为roles
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
#         print(index)
#         # 更新文档
#         roles_collection.update_one(
#             {'_id': role['_id']},
#             {'$set': {
#                 'id': int(index),  # 更新id为新的ObjectId
#                 # 'create_time': create_time,
#                 # 'update_time': update_time,
#                 'is_deleted': is_deleted
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


from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import Field
from datetime import datetime
from typing import Union

from models import Spur, AntCalibCrossFreq, Calibration, Eirp, RoleTest, Pattern


class RoleBaseDocument(Document):
    role_name: str = Field(..., max_length=50)
    role_code: str = Field(..., max_length=50)
    description: str = Field(...)
    create_time: Union[datetime, str] = Field(...)
    update_time: Union[datetime, str] = Field(...)
    is_deleted: bool = Field(default=False)  # 将 is_deleted 统一为布尔类型

    class Settings:
        arbitrary_types_allowed = True
        orm_mode = True


class RoleWbsite(RoleBaseDocument):
    id: Union[int, str] = Field(..., primary_field=True, alias='id')

    class Settings:
        name = "roles"
        database = "wbsite"


async def main():
    # 初始化数据库连接
    client_test_data = AsyncIOMotorClient("mongodb://localhost:27017/test_data")
    client_wbsite = AsyncIOMotorClient("mongodb://localhost:27017/wbsite")

    # 对每个数据库进行Beanie初始化
    await init_beanie(database=client_test_data.test_data,
                      document_models=[Spur, AntCalibCrossFreq, Calibration, Eirp, Pattern, RoleTest])
    await init_beanie(database=client_wbsite.wbsite, document_models=[RoleWbsite])

    # 更新文档
    # async for role in Calibration.find():
    #     if isinstance(role.create_time, str):
    #         role.create_time = datetime.strptime(role.create_time, "%d/%m/%Y %H:%M:%S")
    #     if isinstance(role.update_time, str):
    #         role.update_time = datetime.strptime(role.update_time, "%d/%m/%Y %H:%M:%S")
    #     role.is_deleted = bool(int(role.is_deleted))  # 从整型转换为布尔型
    #     await role.save()

    # 查询并打印更新后的文档
    print("\nUpdated Documents:")
    async for role in Calibration.find():
        print(role)
        # print(f"ID: {role.id}, Role Name: {role.role_name}, Create Time: {role.create_time}, "
        #       f"Update Time: {role.update_time}, Is Deleted: {role.is_deleted}")


if __name__ == "__main__":
    asyncio.run(main())
    # print(uuid.uuid4().hex)
