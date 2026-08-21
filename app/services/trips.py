import logging
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.trips import Trips
from app.schemas.trips import TripReq
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

async def create_trip(data: TripReq, user_id: uuid.UUID, db: AsyncSession):
    try:
        trip = Trips(
            destination=data.destination,
            days=data.days,
            budget=data.budget,
            trip_style=data.trip_style,
            user_id=user_id
        )
        db.add(trip)
        await db.commit()
        await db.refresh(trip)
        return trip
    except Exception as e:
        await db.rollback()
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))
async def get_all_trips(user_id: uuid.UUID, db: AsyncSession):
    try:
        result = await db.execute(select(Trips).where(Trips.user_id == user_id))
        return result.scalars().all()
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))

async def get_trip_by_id(trip_id: uuid.UUID, user_id: uuid.UUID, db: AsyncSession):
    result = await db.execute(
        select(Trips).where(Trips.id == trip_id, Trips.user_id == user_id)
    )
    trip = result.scalar_one_or_none()
    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
    return trip

async def update_trip(trip_id: uuid.UUID, data: TripReq, user_id: uuid.UUID, db: AsyncSession):
    try:
        trip = await get_trip_by_id(trip_id, user_id, db)
        trip.destination = data.destination
        trip.days = data.days
        trip.budget = data.budget
        trip.trip_style = data.trip_style
        await db.commit()
        await db.refresh(trip)
        return trip
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))


async def delete_trip(trip_id: uuid.UUID, user_id: uuid.UUID, db: AsyncSession):
    try:
        trip = await get_trip_by_id(trip_id, user_id, db)
        await db.delete(trip)
        await db.commit()
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))