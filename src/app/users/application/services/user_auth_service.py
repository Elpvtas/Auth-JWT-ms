# application/auth_service.py

from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException

from src.app.users.domain.entities.user_auth import UserInDB
from src.app.users.domain.repositories.user_auth_repository import UserAuthRepository
from src.app.users.domain.repositories.user_repository import UserRepository

SECRET_KEY = "113e76771656fd6cbbe0fb52e60ba839f52882bfc9f699bae42b910df654ce6d"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserAuthService:
    def __init__(self, user_repo: UserAuthRepository):
        self.user_repo = user_repo

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(self, username: str, password: str) -> UserInDB:
        user = self.user_repo.get_user(username)
        if not user or not self.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        return user

    def create_token(self, data: dict, time_expire: Optional[timedelta] = None):
        data_copy = data.copy()
        expire = datetime.utcnow() + (time_expire or timedelta(minutes=15))
        data_copy.update({"exp": expire})
        return jwt.encode(data_copy, key=SECRET_KEY, algorithm=ALGORITHM)

    def decode_token(self, token: str) -> str:
        from jose import JWTError
        try:
            payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return username
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def get_user(self, username: str):
        return self.user_repo.get_user(username)
