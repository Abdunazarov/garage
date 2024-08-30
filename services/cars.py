from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, delete
from sqlalchemy.future import select
from models import Car
from schemas.cars import CarCreate

async def create_car(session: AsyncSession, car_data: CarCreate):
    stmt = insert(Car).values(**car_data.model_dump(exclude_unset=True)).returning(Car)
    result = await session.execute(stmt)
    return result.scalars().first()

async def update_car(session: AsyncSession, car_id: int, car_data: CarCreate):
    stmt = (
        update(Car)
        .where(Car.id == car_id)
        .values(**car_data.model_dump(exclude_unset=True))
        .returning(Car)
    )
    result = await session.execute(stmt)
    return result.scalar()

async def delete_car(session: AsyncSession, car_id: int):
    stmt = delete(Car).where(Car.id == car_id)
    await session.execute(stmt)

async def get_cars(session: AsyncSession):
    result = await session.execute(select(Car))
    return result.scalars().all()
