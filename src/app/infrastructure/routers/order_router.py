# src/app/infrastructure/api/routes/order_routes.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, Body
from fastapi.security import OAuth2PasswordBearer

from src.app.application.services.generic_service import GenericService
from src.app.domain.entities.order import Order
from src.app.infrastructure.repositories.order_repository_impl import OrdenRepositoryImpl
from src.app.domain.entities.user import User
from src.app.infrastructure.dependencies.auth_dependencies import get_current_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


# Dependency para instanciar el servicio genérico de Orden
def get_orden_service() -> GenericService[Order]:
    repository = OrdenRepositoryImpl()
    return GenericService[Order](repository)


# Obtener todas las órdenes
@router.get("/", response_model=List[Order], summary="Get All Ordenes")
def get_all_ordenes(
    service: GenericService[Order] = Depends(get_orden_service),
    current_user: User = Depends(get_current_user)
):
    return service.get_all()


# Obtener orden por ID
@router.get("/{orden_id}", response_model=Order, summary="Get Orden by ID")
def get_orden_by_id(
    orden_id: int = Path(..., description="The ID of the orden to retrieve"),
    service: GenericService[Order] = Depends(get_orden_service),
    current_user: User = Depends(get_current_user)
):
    orden = service.get_by_id(orden_id)
    if not orden:
        raise HTTPException(status_code=404, detail="Orden not found")
    return orden


# Crear una nueva orden
@router.post("/", response_model=Order, status_code=201, summary="Create New Orden")
def create_orden(
    orden: Order = Body(..., description="Orden to create"),
    service: GenericService[Order] = Depends(get_orden_service),
    current_user: User = Depends(get_current_user)
):
    return service.create(orden)


# Actualizar una orden existente
@router.put("/{orden_id}", response_model=Order, summary="Update Orden by ID")
def update_orden(
    orden_id: int,
    orden: Order = Body(...),
    service: GenericService[Order] = Depends(get_orden_service),
    current_user: User = Depends(get_current_user)
):
    updated_orden = service.update(orden_id, orden)
    if not updated_orden:
        raise HTTPException(status_code=404, detail="Orden not found")
    return updated_orden


# Eliminar una orden (soft delete)
@router.delete("/{orden_id}", response_model=dict, summary="Delete Orden by ID")
def delete_orden(
    orden_id: int,
    service: GenericService[Order] = Depends(get_orden_service),
    current_user: User = Depends(get_current_user)
):
    success = service.delete(orden_id)
    if not success:
        raise HTTPException(status_code=404, detail="Orden not found or already deleted")
    return {"detail": "Orden deleted successfully"}
