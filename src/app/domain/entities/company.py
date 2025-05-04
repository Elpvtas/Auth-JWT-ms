from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class Company(BaseModel):
    id: Optional[int]
    nombre: str
    descripcion: Optional[str]
    sector_economico_id: Optional[int]
    created_at: Optional[datetime] = None
    update_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
