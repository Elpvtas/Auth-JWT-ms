from pydantic import  BaseModel,Field
from typing import Union ,Optional


class UserAuth(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(UserAuth):
    hashed_password: str