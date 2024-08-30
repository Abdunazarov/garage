from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
import services.rentals as rental_service
import schemas.rentals as rental_schema
from services.authentication import get_current_user
from models import User

router = APIRouter(tags=["RENTALS"])

@router.post("/", response_model=rental_schema.Rental)
async def create_rental(rental: rental_schema.RentalCreate, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    renter = await rental_service.get_renter_by_id(session, rental.renter_id)
    if not renter:
        raise HTTPException(status_code=404, detail="Renter not found")
    
    car = await rental_service.get_car_by_id(session, rental.renter_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    
    session_rental = await rental_service.create_rental(session, rental)
    return session_rental

@router.put("/{rental_id}", response_model=rental_schema.Rental)
async def update_rental(rental_id: int, rental: rental_schema.RentalUpdate, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    updated_rental = await rental_service.update_rental(session, rental_id, rental)
    if not updated_rental:
        raise HTTPException(status_code=404, detail="Rental not found")
    return updated_rental

@router.delete("/{rental_id}", status_code=204)
async def delete_rental(rental_id: int, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    rental = await session.get(rental_service.Rental, rental_id)
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")
    
    await rental_service.delete_rental(session, rental_id)
    return {"detail": "Rental deleted successfully"}

@router.get("/", response_model=List[rental_schema.Rental])
async def get_rentals(renter_id: Optional[int] = None, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    rentals = await rental_service.get_rentals(session, renter_id)
    return rentals

@router.get("/search/{name}", response_model=List[rental_schema.Rental])
async def get_rentals(name: str, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    rentals = await rental_service.get_rentals_by_renter_name(session, name)
    return rentals
