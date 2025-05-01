from abc import ABC

from src.app.domain.repositories.user_repository import UserRepository
from src.app.infrastructure.database.db_connection_factory import DatabaseConectionFactory
from typing import List,Optional
from src.app.domain.entities.user import User, UserInDB
from datetime import datetime
from src.app.domain.value_object.username_user import UsernameUser


class UserRepositoryImpl(UserRepository, ABC):

  def __init__(self):
    # Inicializamos con un diccionario de ejemplo de usuarios
    self.users = {
      "prueba": {
        "id": 1,
        "username": "prueba",
        "full_name": "Usuario Prueba",
        "email": "usuario@gmail.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
        "rol": 1,
        "city": 1,
        "update_at": datetime.utcnow(),
        "deleted_at": None
      }
    }

  def get_user(self, username: str) -> UserInDB:
    if username in self.users:
      return UserInDB(**self.users[username])
    return None

  def get_all(self) -> List[User]:
    connection = DatabaseConectionFactory.get_connection()
    try:
      with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Usuario")
        row = cursor.fetchall()
        return [
          User(
            id=user[0],
            username=user[1],
            full_name=user[2],
            address=user[3],
            email=user[4],
            hashed_password=user[5],
            disabled=user[6],
            rol=user[7],
            city=user[8],
            update_at=user[9],
            deleted_at=user[10],
          ) for user in row]

    finally:
      DatabaseConectionFactory.release_connection(connection)

  def get_by_id(self, user_id: int) -> Optional[User]:
    connection = DatabaseConectionFactory.get_connection()

    try:
      pass
    finally:
      DatabaseConectionFactory.release_connection()

  def create(self, user: User) -> User:
    connection = DatabaseConectionFactory.get_connection()

    try:
      pass
    finally:
      DatabaseConectionFactory.release_connection()

  def update(self, user_id: int, user: User) -> Optional[User]:
    connection = DatabaseConectionFactory.get_connection()

    try:
      pass
    finally:
      DatabaseConectionFactory.release_connection()

  def delete(self, user_id: int) -> bool:
    connection = DatabaseConectionFactory.get_connection()

    try:
      pass
    finally:
      DatabaseConectionFactory.release_connection()

