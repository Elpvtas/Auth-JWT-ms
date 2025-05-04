from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, Body
from fastapi.security import OAuth2PasswordBearer

from src.app.application.services.generic_service import GenericService
from src.app.domain.entities.company import Company
from src.app.infrastructure.repositories.company_repository_impl import CompanyRepositoryImpl
from src.app.domain.entities.user import User
from src.app.infrastructure.dependencies.auth_dependencies import get_current_user

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


# Dependency para instanciar el servicio genérico de compañía
def get_company_service() -> GenericService[Company]:
    repository = CompanyRepositoryImpl()
    return GenericService[Company](repository)


# Obtener todas las empresas
@router.get("/", response_model=List[Company], summary="Get All Companies")
def get_all_companies(
    service: GenericService[Company] = Depends(get_company_service),
    current_user: User = Depends(get_current_user)
):
    return service.get_all()


# Obtener empresa por ID
@router.get("/{company_id}", response_model=Company, summary="Get Company by ID")
def get_company_by_id(
    company_id: int = Path(..., description="The ID of the company to retrieve"),
    service: GenericService[Company] = Depends(get_company_service),
    current_user: User = Depends(get_current_user)
):
    company = service.get_by_id(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


# Crear una nueva empresa
@router.post("/", response_model=Company, status_code=201, summary="Create New Company")
def create_company(
    company: Company = Body(..., description="Company to create"),
    service: GenericService[Company] = Depends(get_company_service),
    current_user: User = Depends(get_current_user)
):
    return service.create(company)


# Actualizar una empresa existente
@router.put("/{company_id}", response_model=Company, summary="Update Company by ID")
def update_company(
    company_id: int,
    company: Company = Body(...),
    service: GenericService[Company] = Depends(get_company_service),
    current_user: User = Depends(get_current_user)
):
    updated_company = service.update(company_id, company)
    if not updated_company:
        raise HTTPException(status_code=404, detail="Company not found")
    return updated_company


# Eliminar una empresa
@router.delete("/{company_id}", response_model=dict, summary="Delete Company by ID")
def delete_company(
    company_id: int,
    service: GenericService[Company] = Depends(get_company_service),
    current_user: User = Depends(get_current_user)
):
    success = service.delete(company_id)
    if not success:
        raise HTTPException(status_code=404, detail="Company not found or already deleted")
    return {"detail": "Company deleted successfully"}
