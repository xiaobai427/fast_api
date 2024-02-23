from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional, Type
from beanie import Document
from pymongo import ReturnDocument

TCreateRequest = TypeVar('TCreateRequest')
TResponse = TypeVar('TResponse')


class BaseDatabaseOperations(ABC, Generic[TCreateRequest, TResponse]):

    @staticmethod
    async def get_next_sequence(model: Type[Document]) -> int:
        """
        Get the next sequence number for a given model.
        """
        sequence_name = model.__name__  # Using model class name as the sequence identifier
        db = model.get_motor_collection().database
        counters_collection = db.get_collection('counters')

        result = await counters_collection.find_one_and_update(
            {"_id": sequence_name},
            {"$inc": {"sequence_value": 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        return result["sequence_value"]

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
