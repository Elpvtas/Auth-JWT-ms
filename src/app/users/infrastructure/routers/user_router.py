from fastapi import  APIRouter , Depends
from typing import List
from src.app.users.domain.entities.user import User
from src.app.users.application.services.user_service import UserService
from src.app.users.infrastructure.repositories.user_repository_impl import UserRepositoryImpl

router = APIRouter()

def get_user_service():
   repository = UserRepositoryImpl()
   return UserService(repository)

@router.get("/" , response_model= List[User],summary="Get All Users")
def get_all_users(service: UserService = Depends(get_user_service)):
  return service.get_all()


