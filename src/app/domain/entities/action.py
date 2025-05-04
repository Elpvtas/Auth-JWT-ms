from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class Accion(BaseModel):
  id: Optional[int]
  nombre: str
  valor: Optional[float] = None
  fecha_hora: Optional[datetime] = None
  empresa_id: Optional[int] = None

