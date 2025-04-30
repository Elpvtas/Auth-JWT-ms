from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta

from src.app.users.application.services.user_auth_service import UserAuthService
from src.app.users.infrastructure.repositories.user_auth_repository_impl import UserAuthRepositoryImpl
from src.app.users.domain.entities.user_auth import UserAuth

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_user_auth_service() -> UserAuthService:
    repo = UserAuthRepositoryImpl()
    return UserAuthService(repo)

@router.post(
    "/token",
    summary="Login and generate access token",
    response_model=dict,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: UserAuthService  = Depends(get_user_auth_service),
):
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    access_token = auth_service.create_token(
        {"sub": user.username},
        timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get(
    "/me",
    response_model=UserAuth,
    summary="Get current user info"
)
def get_current_user(
    token: str                 = Depends(oauth2_scheme),
    auth_service: UserAuthService = Depends(get_user_auth_service),
):
    # Decodifica el token y extrae el username
    username = auth_service.decode_token(token)
    # Recupera el usuario (añade este método en tu servicio o usa repo)
    try:
        user = auth_service.get_user(username)
    except AttributeError:
        # Si no lo tienes en el servicio, haz:
        user = auth_service.user_repo.get_user(username)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user
