from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic

T = TypeVar('T')

class CrudRepository(ABC, Generic[T]):

    @abstractmethod
    def get_all(self) -> List[T]:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        pass

    @abstractmethod
    def create(self, entity: T) -> T:
        pass

    @abstractmethod
    def update(self, entity_id: int, entity: T) -> Optional[T]:
        pass

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        pass
