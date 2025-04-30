from src.app.users.domain.repositories.user_auth_repository import UserAuthRepository
from src.app.users.domain.entities.user_auth import UserInDB

class UserAuthRepositoryImpl(UserAuthRepository):
    def __init__(self):
        self.users = {
            "prueba": {
                "username": "prueba",
                "full_name": "Usuario Prueba",
                "email": "usuario@gmail.com",
                "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
                "disabled": False,
            }
        }

    def get_user(self, username: str) -> UserInDB:
        if username in self.users:
            return UserInDB(**self.users[username])
        return None
