from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
import services.renters as renter_service
import schemas.renters as renter_schema
from services.authentication import get_current_user
from models import User

router = APIRouter(tags=["RENTERS"])

@router.post("/", response_model=renter_schema.Renter)
async def create_renter(renter: renter_schema.RenterCreate, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    return await renter_service.create_renter(session, renter)

@router.put("/{renter_id}", response_model=renter_schema.Renter)
async def update_renter(renter_id: int, renter: renter_schema.RenterUpdate, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    updated_renter = await renter_service.update_renter(session, renter_id, renter)
    if not updated_renter:
        raise HTTPException(status_code=404, detail="Renter not found")
    return updated_renter

@router.delete("/{renter_id}", status_code=204)
async def delete_renter(renter_id: int, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    renter = await session.get(renter_service.Renter, renter_id)
    if not renter:
        raise HTTPException(status_code=404, detail="Renter not found")
    
    await renter_service.delete_renter(session, renter_id)
    return {"detail": "Renter deleted successfully"}

@router.get("/", response_model=List[renter_schema.Renter])
async def get_renters(session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    return await renter_service.get_renters(session)
