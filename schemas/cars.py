from pydantic import BaseModel
from typing import Optional

class CarBase(BaseModel):
    car_name: str
    owner_name: str

class CarCreate(CarBase):
    pass

class Car(CarBase):
    id: int
    
class CarUpdate(BaseModel):
    car_name: Optional[str] = None
    owner_name: Optional[str] = None

