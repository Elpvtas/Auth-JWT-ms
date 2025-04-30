from pydantic import  BaseModel,Field
from typing import Union

#THIS IS FOR A EXCEPTION CASES OR WORK VALIDATION IN THE MODEL
from src.app.andina.domain.value_object.username_user import UsernameUser

class User(BaseModel):
  id:int = Field(...,description="Id usuario")
  username: UsernameUser
  full_name: Union[str, None] = None
  address:str
  email: Union[str, None] = None
  hashed_password:str = Field(..., description="Password user")
  disabled: Union[bool, None] = None
