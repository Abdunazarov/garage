from pydantic import BaseModel
from datetime import date
from typing import Optional
from enum import Enum

class RentalStatus(str, Enum):
    DEPOSIT_MADE = "Дал залог"
    IN_PROGRESS = "В процессе"
    PAID = "Оплачено"
    DEBT = "Долг"

class RentalCreate(BaseModel):
    renter_id: int
    car_id: int
    issue_date: date
    return_date: date
    total_amount: float
    payment_method: str
    investor_percentage: float
    deposit: float
    mileage: Optional[float] = None
    fuel_cost: Optional[float] = None
    status: RentalStatus = RentalStatus.DEBT
    other_expenses: Optional[float] = None

class RentalUpdate(BaseModel):
    renter_id: Optional[int] = None
    car_id: Optional[int] = None
    issue_date: Optional[date] = None
    return_date: Optional[date] = None
    total_amount: Optional[float] = None
    payment_method: Optional[str] = None
    investor_percentage: Optional[float] = None
    investor_profit: Optional[int] = None
    deposit: Optional[float] = None
    mileage: Optional[float] = None
    fuel_cost: Optional[float] = None
    status: Optional[RentalStatus] = None
    other_expenses: Optional[float] = None

class Rental(BaseModel):
    id: int
    renter_id: int
    car_id: int
    issue_date: date
    return_date: date
    total_amount: float
    investor_profit: Optional[int] = None
    investor_percentage: Optional[float] = None
    payment_method: str
    deposit: float
    mileage: Optional[float] = None
    fuel_cost: Optional[float] = None
    other_expenses: Optional[float] = None
    status: Optional[RentalStatus] = None
