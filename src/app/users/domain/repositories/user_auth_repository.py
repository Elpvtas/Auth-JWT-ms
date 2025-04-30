# ports/user_repository.py
from src.app.users.domain.entities.user_auth import UserInDB
from abc import ABC, abstractmethod

class UserAuthRepository(ABC):
    @abstractmethod
    def get_user(self, username: str) -> UserInDB:
        pass
