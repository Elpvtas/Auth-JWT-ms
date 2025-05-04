# src/app/domain/entities/contrato.py

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Contract:
    numero_contrato: int
    fecha_hora_inicio: datetime
    fecha_hora_fin: Optional[datetime]
    comision: float
    inversionista_id: int
    comisionista_id: int
    created_at: Optional[datetime] = None
    update_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
