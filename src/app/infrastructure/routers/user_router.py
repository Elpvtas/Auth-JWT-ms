from datetime import timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.app.application.services.user_service import UserService
from src.app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from src.app.domain.entities.user import User


# Router and OAuth2 scheme initialization
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


# Dependency to instantiate the UserService
def get_user_service():
    repository = UserRepositoryImpl()
    return UserService(repository)


# Dependency to get the current authenticated user from the token
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
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token or authentication failed") from e


# Route to get all users (requires authentication)
@router.get("/", response_model=List[User], summary="Get All Users")
def get_all_users(
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    return service.get_all()


# Route to login and generate an access token
@router.post("/token", summary="Login and generate access token", response_model=dict)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: UserService = Depends(get_user_service)
):
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    access_token = auth_service.create_token(
        {"sub": user.username}, timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Route to get current user's info (requires authentication)
@router.get("/me", response_model=User, summary="Get current user info")
def get_current_user_info(
    token: str = Depends(oauth2_scheme),
    auth_service: UserService = Depends(get_user_service)
):
    username = auth_service.decode_token(token)
    user = auth_service.get_user(username)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


# Route to get user by ID (requires authentication)
@router.get("/{user_id}", response_model=User, summary="Get user by ID")
def get_user_by_id(
    user_id: int = Path(..., description="The ID of the user to retrieve"),
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    user = service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Route to create a new user (requires authentication)
@router.post("/", response_model=User, status_code=201, summary="Create new user")
def create_user(
    user: User = Body(..., description="User to create"),
    service: UserService = Depends(get_user_service)
):
    return service.create(user)


# Route to update an existing user by ID (requires authentication)
@router.put("/{user_id}", response_model=User, summary="Update user by ID")
def update_user(
    user_id: int,
    user: User = Body(...),
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    updated_user = service.update(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


# Route to delete a user by ID (requires authentication)
@router.delete("/{user_id}", response_model=dict, summary="Delete user by ID")
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    success = service.delete(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found or already deleted")
    return {"detail": "User deleted successfully"}
