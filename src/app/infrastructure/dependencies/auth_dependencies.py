from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from src.app.domain.entities.user import User
from src.app.application.services.user_service import UserService
from src.app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

def get_user_service():
    repository = UserRepositoryImpl()
    return UserService(repository)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: UserService = Depends(get_user_service)
) -> User:
    try:
        username = service.decode_token(token)
        user = service.get_user(username)
        if not user or user.disabled:
            raise HTTPException(status_code=400, detail="Inactive or invalid user")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
