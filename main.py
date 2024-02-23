from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from log_manager import log_manager
# 假设的模型和服务导入
from models import RoleTest, Spur, AntCalibCrossFreq, Calibration, Eirp, Pattern, RoleWbsite
from api.role_api import router as role_router

# 全局MongoDB客户端实例
client_test_data: AsyncIOMotorClient = None
client_wbsite: AsyncIOMotorClient = None

app = FastAPI()


@app.on_event("startup")
async def app_init():
    global client_test_data, client_wbsite
    log_manager.debug("Initializing MongoDB client...")
    # 创建MongoDB客户端实例
    client_test_data = AsyncIOMotorClient("mongodb://localhost:27017/test_data")
    client_wbsite = AsyncIOMotorClient("mongodb://localhost:27017/wbsite")
    log_manager.debug("MongoDB client initialized.")
    log_manager.debug("Initializing routes...")

    # Beanie初始化
    await init_beanie(database=client_test_data.test_data,
                      document_models=[Spur, AntCalibCrossFreq, Calibration, Eirp, Pattern, RoleTest])
    await init_beanie(database=client_wbsite.wbsite, document_models=[RoleWbsite])


@app.on_event("shutdown")
async def app_shutdown():

    log_manager.debug("Shutdown event occurred. Closing MongoDB connections.")
    # 关闭MongoDB客户端连接
    client_test_data.close()
    client_wbsite.close()
    log_manager.close()


# 包含路由
app.include_router(role_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
