from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class User(BaseModel):
    id: int = Field(..., description="Id del usuario")
    username: str
    full_name: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    hashed_password: str = Field(..., description="Contraseña hasheada del usuario")
    disabled: Optional[bool] = None
    rol: Optional[int] = None
    city: Optional[int] = None
    update_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


class UserInDB(User):
  hashed_password: str
