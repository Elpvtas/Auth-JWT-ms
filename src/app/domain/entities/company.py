from dataclasses import Field
from typing import Optional

from pydantic import BaseModel


class Company(BaseModel):
  id:int = Field(..., description ="Company Id")
  name_company = str
  business_sector = Optional[str] = None
