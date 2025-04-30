from src.app.users.domain.repositories.user_repository import UserRepository
from src.app.infrastructure.database.db_connection_factory import DatabaseConectionFactory
from typing import List,Optional
from src.app.users.domain.entities.user import User

from src.app.users.domain.value_object.username_user import UsernameUser


class UserRepositoryImpl(UserRepository):

    def get_all(self) -> List[User]:
        connection = DatabaseConectionFactory.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users")
                row = cursor.fetchAll()
                return [
                    User(
                        id= row[0],
                        username = UsernameUser(value= row[1]),
                        full_name = row[2],
                        address =row[3],
                        email  =row[4],
                        hashed_password =row[5],
                        disabled =row[6],
                        rol =row[7],
                        city =row[8],
                        update_at =row[9],
                        deleted_at =row[10],
                    ) for user in row]


        finally:
            DatabaseConectionFactory.release_connection()



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
