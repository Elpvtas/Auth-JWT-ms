# src/app/infrastructure/api/routes/contract_routes.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, Body
from fastapi.security import OAuth2PasswordBearer

from src.app.application.services.generic_service import GenericService
from src.app.domain.entities.contract import Contract
from src.app.infrastructure.repositories.contract_repository_impl import ContratoRepositoryImpl
from src.app.domain.entities.user import User
from src.app.infrastructure.dependencies.auth_dependencies import get_current_user

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


# Dependency para instanciar el servicio genérico de Contrato
def get_contrato_service() -> GenericService[Contract]:
    repository = ContratoRepositoryImpl()
    return GenericService[Contract](repository)


# Obtener todos los contratos
@router.get("/", response_model=List[Contract], summary="Get All Contratos")
def get_all_contratos(
    service: GenericService[Contract] = Depends(get_contrato_service),
    current_user: User = Depends(get_current_user)
):
    return service.get_all()


# Obtener contrato por ID
@router.get("/{numero_contrato}", response_model=Contract, summary="Get Contrato by ID")
def get_contrato_by_id(
    numero_contrato: int = Path(..., description="The ID of the contrato to retrieve"),
    service: GenericService[Contract] = Depends(get_contrato_service),
    current_user: User = Depends(get_current_user)
):
    contrato = service.get_by_id(numero_contrato)
    if not contrato:
        raise HTTPException(status_code=404, detail="Contrato not found")
    return contrato


# Crear un nuevo contrato
@router.post("/", response_model=Contract, status_code=201, summary="Create New Contrato")
def create_contrato(
    contrato: Contract= Body(..., description="Contrato to create"),
    service: GenericService[Contract] = Depends(get_contrato_service),
    current_user: User = Depends(get_current_user)
):
    return service.create(contrato)


# Actualizar un contrato existente
@router.put("/{numero_contrato}", response_model=Contract, summary="Update Contrato by ID")
def update_contrato(
    numero_contrato: int,
    contrato: Contract = Body(...),
    service: GenericService[Contract] = Depends(get_contrato_service),
    current_user: User = Depends(get_current_user)
):
    updated_contrato = service.update(numero_contrato, contrato)
    if not updated_contrato:
        raise HTTPException(status_code=404, detail="Contrato not found")
    return updated_contrato


# Eliminar un contrato (soft delete)
@router.delete("/{numero_contrato}", response_model=dict, summary="Delete Contrato by ID")
def delete_contrato(
    numero_contrato: int,
    service: GenericService[Contract] = Depends(get_contrato_service),
    current_user: User = Depends(get_current_user)
):
    success = service.delete(numero_contrato)
    if not success:
        raise HTTPException(status_code=404, detail="Contrato not found or already deleted")
    return {"detail": "Contrato deleted successfully"}
