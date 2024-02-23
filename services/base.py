# 引入泛型类型变量和基类
from abc import abstractmethod, ABC
from typing import TypeVar, Generic, List, Optional

TCreateRequest = TypeVar('TCreateRequest')
TResponse = TypeVar('TResponse')


class BaseDatabaseOperations(ABC, Generic[TCreateRequest, TResponse]):
    @abstractmethod
    async def create(self, create_data: TCreateRequest) -> TResponse:
        pass

    @abstractmethod
    async def get_all(self) -> List[TResponse]:
        pass

    @abstractmethod
    async def search(self, name: Optional[str] = None, code: Optional[str] = None) -> List[TResponse]:
        pass

    @abstractmethod
    async def get_by_id(self, record_id: int) -> TResponse:
        pass

    @abstractmethod
    async def update(self, record_id: int, update_data: TCreateRequest) -> TResponse:
        pass

    @abstractmethod
    async def delete(self, record_id: int) -> None:
        pass
