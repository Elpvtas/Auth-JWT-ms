from abc import ABC

from src.app.application.services.user_service import pwd_context
from src.app.domain.repositories.crud_repository import CrudRepository
from src.app.infrastructure.database.db_connection_factory import DatabaseConectionFactory
from typing import List, Optional
from src.app.domain.entities.user import User, UserInDB
from datetime import datetime
from passlib.context import CryptContext


class UserRepositoryImpl(CrudRepository[User], ABC):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_user(self, username: str) -> Optional[UserInDB]:
      connection = DatabaseConectionFactory.get_connection()
      try:
        with connection.cursor() as cursor:
          cursor.execute("SELECT * FROM Usuario WHERE username = %s", (username,))
          row = cursor.fetchone()
          if row:
            return UserInDB(
              id=row[0],
              username=row[1],
              full_name=row[2],
              address=row[3],
              email=row[4],
              hashed_password=row[5],
              disabled=row[6],
              rol=row[7],
              city=row[8],
              update_at=row[9],
              deleted_at=row[10],
            )
          return None
      finally:
        DatabaseConectionFactory.release_connection(connection)

    def get_all(self) -> List[User]:
        connection = DatabaseConectionFactory.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Usuario")
                rows = cursor.fetchall()
                return [
                    User(
                        id=row[0],
                        username=row[1],
                        full_name=row[2],
                        address=row[3],
                        email=row[4],
                        hashed_password=row[5],
                        disabled=row[6],
                        rol=row[7],
                        city=row[8],
                        update_at=row[9],
                        deleted_at=row[10],
                    ) for row in rows
                ]
        finally:
            DatabaseConectionFactory.release_connection(connection)

    def get_by_id(self, user_id: int) -> Optional[User]:
        connection = DatabaseConectionFactory.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Usuario WHERE id = %s", (user_id,))
                row = cursor.fetchone()
                if row:
                    return User(
                        id=row[0],
                        username=row[1],
                        full_name=row[2],
                        address=row[3],
                        email=row[4],
                        hashed_password=row[5],
                        disabled=row[6],
                        rol=row[7],
                        city=row[8],
                        update_at=row[9],
                        deleted_at=row[10],
                    )
                return None
        finally:
            DatabaseConectionFactory.release_connection(connection)

    def create(self, user: User) -> User:
      connection = DatabaseConectionFactory.get_connection()
      try:
        with connection.cursor() as cursor:
          cursor.execute("""
                  INSERT INTO Usuario (username, full_name, address, email, hashed_password, disabled, rol, city, update_at, deleted_at)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              """, (
            user.username,
            user.full_name,
            user.address,
            user.email,
            self.pwd_context.hash(user.hashed_password),
            user.disabled,
            user.rol,
            user.city,
            user.update_at,
            user.deleted_at,
          ))
          user_id = cursor.lastrowid
          connection.commit()
          user.id = user_id
          return user
      finally:
        DatabaseConectionFactory.release_connection(connection)

    def update(self, user_id: int, user: User) -> Optional[User]:
        connection = DatabaseConectionFactory.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE Usuario SET
                        username = %s,
                        full_name = %s,
                        address = %s,
                        email = %s,
                        hashed_password = %s,
                        disabled = %s,
                        rol = %s,
                        city = %s,
                        update_at = %s,
                        deleted_at = %s
                    WHERE id = %s
                """, (
                    user.username,
                    user.full_name,
                    user.address,
                    user.email,
                    user.hashed_password,
                    user.disabled,
                    user.rol,
                    user.city,
                    user.update_at,
                    user.deleted_at,
                    user_id,
                ))
                connection.commit()
                return self.get_by_id(user_id)
        finally:
            DatabaseConectionFactory.release_connection(connection)

    def delete(self, user_id: int) -> bool:
        if user_id is not 1:
          connection = DatabaseConectionFactory.get_connection()
          try:
              with connection.cursor() as cursor:
                  cursor.execute("DELETE FROM Usuario WHERE id = %s", (user_id,))
                  affected_rows = cursor.rowcount
                  connection.commit()
                  return affected_rows > 0
          finally:
              DatabaseConectionFactory.release_connection(connection)
        else:
          return False
