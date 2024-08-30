from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, delete
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from models import Rental, Renter, Car
from schemas.rentals import RentalCreate
from typing import Optional

async def get_renter_by_id(session: AsyncSession, renter_id: int):
    result = await session.execute(select(Renter).filter(Renter.id == renter_id))
    return result.scalars().first()

async def get_car_by_id(session: AsyncSession, car_id: int):
    result = await session.execute(select(Car).filter(Car.id == car_id))
    return result.scalars().first()

async def create_rental(session: AsyncSession, rental_data: RentalCreate):
    stmt = insert(Rental).values(**rental_data.model_dump()).returning(Rental)
    result = await session.execute(stmt)
    await session.commit()
    return result.scalars().first()

async def update_rental(session: AsyncSession, rental_id: int, rental_data: RentalCreate):
    stmt = (
        update(Rental)
        .where(Rental.id == rental_id)
        .values(**rental_data.model_dump())
        .execution_options(synchronize_session="fetch")
    )
    await session.execute(stmt)
    await session.commit()
    return await session.get(Rental, rental_id)

async def delete_rental(session: AsyncSession, rental_id: int):
    stmt = delete(Rental).where(Rental.id == rental_id)
    await session.execute(stmt)
    await session.commit()

async def get_rentals(session: AsyncSession, renter_id: Optional[int] = None):
    stmt = select(Rental).options(
        joinedload(Rental.renter),
        joinedload(Rental.car)
    )
    
    if renter_id:
        stmt = stmt.where(Rental.renter_id == renter_id)
    
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_rentals_by_renter_name(session: AsyncSession, renter_name: str):
    stmt = select(Rental).join(Rental.renter).options(
        joinedload(Rental.renter),
        joinedload(Rental.car)
    ).where(Renter.full_name.ilike(f"%{renter_name}%"))
    
    result = await session.execute(stmt)
    return result.scalars().all()

