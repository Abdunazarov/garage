from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, delete
from sqlalchemy.future import select
from models import Renter
from schemas.renters import RenterCreate

async def create_renter(session: AsyncSession, renter_data: RenterCreate):
    stmt = insert(Renter).values(**renter_data.model_dump(exclude_unset=True)).returning(Renter)
    result = await session.execute(stmt)
    return result.scalars().first()

async def update_renter(session: AsyncSession, renter_id: int, renter_data: RenterCreate):
    stmt = (
        update(Renter)
        .where(Renter.id == renter_id)
        .values(**renter_data.model_dump(exclude_unset=True)).returning(Renter)
    )
    result = await session.execute(stmt)
    return result.scalar()

async def delete_renter(session: AsyncSession, renter_id: int):
    stmt = delete(Renter).where(Renter.id == renter_id)
    await session.execute(stmt)

async def get_renters(session: AsyncSession):
    result = await session.execute(select(Renter))
    return result.scalars().all()
