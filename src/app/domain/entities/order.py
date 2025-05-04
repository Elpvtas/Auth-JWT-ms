from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Order(BaseModel):
    id: Optional[int]
    tipo_orden: str
    precio: float
    fecha_hora: datetime
    comision: Optional[float]
    usuario_id: int
    created_at: Optional[datetime]
    update_at: Optional[datetime]
    deleted_at: Optional[datetime]
