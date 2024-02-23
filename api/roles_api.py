from fastapi import APIRouter, Body, Query
from typing import Optional, Union

from api.base import RoleAPIHandler
from common.result import Result
from beanie import PydanticObjectId

from services.role_batabase import RoleCreateRequest


class RoleAPI:
    def __init__(self, db_ops_handler: RoleAPIHandler):
        self.handler = db_ops_handler
        self.router = APIRouter()
        self.register_routes()

    def register_routes(self):
        @self.router.post("/roles/", response_model=Result)
        async def create_role(role_request: RoleCreateRequest):
            return await self.handler.create_role(role_request)

        @self.router.get("/roles/", response_model=Result)
        async def list_roles():
            return await self.handler.list_roles()

        @self.router.get("/roles/search", response_model=Result)
        async def search_roles(role_id: Union[int, str], role_name: Optional[str] = Query(None), role_code: Optional[str] = Query(None)):
            return await self.handler.search_roles(role_id, role_name, role_code)

        @self.router.get("/roles/{role_id}", response_model=Result)
        async def get_role(role_id: Union[int, str, PydanticObjectId]):
            return await self.handler.get_role(role_id)

        @self.router.put("/roles/{role_id}", response_model=Result)
        async def update_role(role_id: Union[int, str], role_request: RoleCreateRequest = Body(...)):
            return await self.handler.update_role(role_id, role_request)

        @self.router.delete("/roles/{role_id}", response_model=Result)
        async def delete_role(role_id: Union[int, str]):
            return await self.handler.delete_role(role_id)

    def get_router(self):
        return self.router
