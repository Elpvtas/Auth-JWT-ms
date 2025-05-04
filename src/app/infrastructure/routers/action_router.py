# src/app/infrastructure/api/routes/accion_routes.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, Body
from fastapi.security import OAuth2PasswordBearer

from src.app.application.services.generic_service import GenericService
from src.app.domain.entities.action import Accion
from src.app.infrastructure.repositories.action_repository_impl import AccionRepositoryImpl
from src.app.domain.entities.user import User
from src.app.infrastructure.dependencies.auth_dependencies import get_current_user

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


# Dependency para instanciar el servicio genérico de Accion
def get_accion_service() -> GenericService[Accion]:
    repository = AccionRepositoryImpl()
    return GenericService[Accion](repository)


# Obtener todas las acciones
@router.get("/", response_model=List[Accion], summary="Get All Acciones")
def get_all_acciones(
    service: GenericService[Accion] = Depends(get_accion_service),
    current_user: User = Depends(get_current_user)
):
    return service.get_all()


# Obtener acción por ID
@router.get("/{accion_id}", response_model=Accion, summary="Get Accion by ID")
def get_accion_by_id(
    accion_id: int = Path(..., description="The ID of the accion to retrieve"),
    service: GenericService[Accion] = Depends(get_accion_service),
    current_user: User = Depends(get_current_user)
):
    accion = service.get_by_id(accion_id)
    if not accion:
        raise HTTPException(status_code=404, detail="Accion not found")
    return accion


# Crear una nueva acción
@router.post("/", response_model=Accion, status_code=201, summary="Create New Accion")
def create_accion(
    accion: Accion = Body(..., description="Accion to create"),
    service: GenericService[Accion] = Depends(get_accion_service),
    current_user: User = Depends(get_current_user)
):
    return service.create(accion)


# Actualizar una acción existente
@router.put("/{accion_id}", response_model=Accion, summary="Update Accion by ID")
def update_accion(
    accion_id: int,
    accion: Accion = Body(...),
    service: GenericService[Accion] = Depends(get_accion_service),
    current_user: User = Depends(get_current_user)
):
    updated_accion = service.update(accion_id, accion)
    if not updated_accion:
        raise HTTPException(status_code=404, detail="Accion not found")
    return updated_accion


# Eliminar una acción
@router.delete("/{accion_id}", response_model=dict, summary="Delete Accion by ID")
def delete_accion(
    accion_id: int,
    service: GenericService[Accion] = Depends(get_accion_service),
    current_user: User = Depends(get_current_user)
):
    success = service.delete(accion_id)
    if not success:
        raise HTTPException(status_code=404, detail="Accion not found or already deleted")
    return {"detail": "Accion deleted successfully"}
