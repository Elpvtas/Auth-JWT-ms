from abc import ABC, abstractmethod
from typing import List,Optional
from src.app.andina.domain.entities.user import User

class UserRepository(ABC):

  @abstractmethod
  def get_all(self) -> List[User]:
    pass

  @abstractmethod
  def get_by_id(self, user_id:int) -> Optional[User]:
    pass

  @abstractmethod
  def create(self, user: User) -> User:
    pass

  @abstractmethod
  def update(self, user_id: int , user: User) -> Optional[User]:
    pass

  @abstractmethod
  def delete(self, user_id:int) -> bool:
    pass
