from pydantic import BaseModel
from typing import Optional

class RenterCreate(BaseModel):
    full_name: str
    phone_number: str

class RenterUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None

class Renter(BaseModel):
    id: int
    full_name: str
    phone_number: str
