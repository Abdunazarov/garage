from pydantic import BaseModel
from datetime import date
from typing import Optional

class RentalCreate(BaseModel):
    renter_id: int
    car_id: int
    issue_date: date
    return_date: date
    total_amount: float
    payment_method: str
    deposit: float
    mileage: Optional[float] = None
    fuel_cost: Optional[float] = None
    other_expenses: Optional[float] = None

class RentalUpdate(BaseModel):
    renter_id: Optional[int] = None
    car_id: Optional[int] = None
    issue_date: Optional[date] = None
    return_date: Optional[date] = None
    total_amount: Optional[float] = None
    payment_method: Optional[str] = None
    deposit: Optional[float] = None
    mileage: Optional[float] = None
    fuel_cost: Optional[float] = None
    other_expenses: Optional[float] = None

class Rental(BaseModel):
    id: int
    renter_id: int
    car_id: int
    issue_date: date
    return_date: date
    total_amount: float
    payment_method: str
    deposit: float
    mileage: Optional[float] = None
    fuel_cost: Optional[float] = None
    other_expenses: Optional[float] = None
