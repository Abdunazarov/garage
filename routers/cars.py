from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
import services.cars as car_service
import schemas.cars as car_schema
from services.authentication import get_current_user
from models import User

router = APIRouter(tags=["CARS"])

@router.post("/", response_model=car_schema.Car)
async def create_car(car: car_schema.CarCreate, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    return await car_service.create_car(session, car)

@router.put("/{car_id}", response_model=car_schema.Car)
async def update_car(car_id: int, car: car_schema.CarUpdate, session: AsyncSession = Depends(get_session)):
    print(car)
    updated_car = await car_service.update_car(session, car_id, car)
    if not updated_car:
        raise HTTPException(status_code=404, detail="Car not found")
    return updated_car

@router.delete("/{car_id}", status_code=204)
async def delete_car(car_id: int, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    car = await session.get(car_service.Car, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    
    await car_service.delete_car(session, car_id)
    return {"detail": "Car deleted successfully"}

@router.get("/", response_model=List[car_schema.Car])
async def get_cars(session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    return await car_service.get_cars(session)
