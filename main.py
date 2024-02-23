from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from api.roles_api import RoleAPI
from log_manager import log_manager, logger
# 假设的模型和服务导入
from models import RoleTest, Spur, AntCalibCrossFreq, Calibration, Eirp, Pattern, RoleWbsite
from api.base import router as role_router, RoleAPIHandler
from services.role_batabase import RoleTestDatabaseOperations, RoleWbsiteDatabaseOperations

# 全局MongoDB客户端实例
client_test_data: AsyncIOMotorClient
client_wbsite: AsyncIOMotorClient

app = FastAPI()

# 假设 RoleTestDatabaseOperations 和 RoleWbsiteDatabaseOperations 已定义
role_api_handler_test = RoleAPIHandler[RoleTestDatabaseOperations](RoleTestDatabaseOperations)
role_api_handler_wbsite = RoleAPIHandler[RoleWbsiteDatabaseOperations](RoleWbsiteDatabaseOperations)

role_api_test = RoleAPI(role_api_handler_test)
role_api_wbsite = RoleAPI(role_api_handler_wbsite)

app.include_router(role_api_test.get_router(), prefix="/test")
app.include_router(role_api_wbsite.get_router(), prefix="/wbsite")


@app.on_event("startup")
async def app_init():
    global client_test_data, client_wbsite
    logger.debug("Initializing MongoDB client...")
    # 创建MongoDB客户端实例
    client_test_data = AsyncIOMotorClient("mongodb://localhost:27017/test_data")
    client_wbsite = AsyncIOMotorClient("mongodb://localhost:27017/wbsite")
    logger.debug("MongoDB client initialized.")
    logger.debug("Initializing routes...")

    # Beanie初始化
    await init_beanie(database=client_test_data.test_data,
                      document_models=[Spur, AntCalibCrossFreq, Calibration, Eirp, Pattern, RoleTest])
    await init_beanie(database=client_wbsite.wbsite, document_models=[RoleWbsite])


@app.on_event("shutdown")
async def app_shutdown():
    logger.debug("Shutdown event occurred. Closing MongoDB connections.")
    # 关闭MongoDB客户端连接
    client_test_data.close()
    client_wbsite.close()


# 包含路由
app.include_router(role_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
