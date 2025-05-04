from typing import TypeVar, Generic
from src.app.domain.repositories.crud_repository import CrudRepository

T = TypeVar("T")  # T es una entidad (Company, User, etc.)

class GenericService(Generic[T]):
    def __init__(self, repository: CrudRepository[T]):
        self.repository = repository

    def get_all(self) -> list[T]:
        return self.repository.get_all()

    def get_by_id(self, entity_id: int) -> T:
        return self.repository.get_by_id(entity_id)

    def create(self, entity: T) -> T:
        return self.repository.create(entity)

    def update(self, entity_id: int, entity: T) -> T:
        return self.repository.update(entity_id, entity)

    def delete(self, entity_id: int) -> bool:
        return self.repository.delete(entity_id)
