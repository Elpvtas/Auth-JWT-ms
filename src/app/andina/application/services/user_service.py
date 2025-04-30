from src.app.andina.domain.repositories.user_repository import UserRepository
from src.app.andina.domain.entities.user import User

class UserService:

  def __init__(self, user_repository : UserRepository):
    self.user_repository = UserRepository

  def get_all(self) -> list[User]:
    return self.user_repository.get_all()

  def get_by_id(self, user_id:int ) -> User:
    return self.user_repository.get_by_id(user_id)

  def create(self,user:User) -> User:
    return self.user_repository.create(user)

  def update(self, user_id:int , user:User) -> User:
    return self.user_repository.update(user_id, user)

  def delete(self, user_id:int) -> bool:
    return self.user_repository.delete(user_id)
