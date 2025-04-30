from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from src.app.users.domain.value_object.username_user import UsernameUser

class User(BaseModel):
    id: int = Field(..., description="Id usuario")
    username: UsernameUser
    full_name: Optional[str] = None
    address: str
    email: Optional[str] = None
    hashed_password: str = Field(..., description="Password user")
    disabled: Optional[bool] = None
    rol: Optional[int] = None
    city: Optional[int] = None
    update_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
