from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, delete, func
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from models import Rental, Renter, Car
from schemas.rentals import RentalCreate
from typing import Optional
from datetime import timedelta, date

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



async def get_dashboard_metrics(session: AsyncSession):
    today = date.today()
    first_day_of_month = today.replace(day=1)

    renters_per_month_query = select(func.count(Rental.id)).filter(Rental.issue_date >= first_day_of_month)
    renters_per_month_result = await session.execute(renters_per_month_query)
    renters_per_month = renters_per_month_result.scalar()

    monthly_cash_query = select(func.sum(Rental.total_amount)).filter(Rental.issue_date >= first_day_of_month)
    monthly_cash_result = await session.execute(monthly_cash_query)
    monthly_cash = monthly_cash_result.scalar() or 0

    monthly_expenses_query = select(func.sum(Rental.other_expenses)).filter(Rental.issue_date >= first_day_of_month)
    monthly_expenses_result = await session.execute(monthly_expenses_query)
    monthly_expenses = monthly_expenses_result.scalar() or 0

    renters_per_day_query = select(func.count(Rental.id)).filter(Rental.issue_date == today)
    renters_per_day_result = await session.execute(renters_per_day_query)
    renters_per_day = renters_per_day_result.scalar()

    daily_cash_query = select(func.sum(Rental.total_amount)).filter(Rental.issue_date == today)
    daily_cash_result = await session.execute(daily_cash_query)
    daily_cash = daily_cash_result.scalar() or 0

    return {
        "renters_per_month": renters_per_month,
        "monthly_cash": monthly_cash,
        "monthly_expenses": monthly_expenses,
        "renters_per_day": renters_per_day,
        "daily_cash": daily_cash,
    }