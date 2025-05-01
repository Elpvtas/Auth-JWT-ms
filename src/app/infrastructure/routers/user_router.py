from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.app.application.services.user_service import UserService
from src.app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from src.app.domain.entities.user import User


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")



def get_user_service():
    repository = UserRepositoryImpl()
    return UserService(repository)


@router.get("/", response_model=List[User], summary="Get All Users")
def get_all_users(service: UserService = Depends(get_user_service)):
    return service.get_all()


@router.post("/token", summary="Login and generate access token", response_model=dict)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: UserService = Depends(get_user_service),
):
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    access_token = auth_service.create_token(
        {"sub": user.username},
        timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=User, summary="Get current user info")
def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: UserService = Depends(get_user_service),  # Asegúrate de que la dependencia esté correcta
):
    username = auth_service.decode_token(token)

    try:
        user = auth_service.get_user(username)
        print(user)
    except AttributeError:
        user = auth_service.user_repository.get_user(username)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user
