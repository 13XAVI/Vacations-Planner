import logging
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.itinerary import Itineraries
from app.models.trips import Trips
from app.schemas.itinerary import itinerary_req
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

async def create_itinerary(data: itinerary_req, user_id: uuid.UUID, db: AsyncSession):
    result = await db.execute(
        select(Trips).where(Trips.id == data.trip_id, Trips.user_id == user_id)
    )
    trip = result.scalar_one_or_none()
    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")

    itinerary = Itineraries(
        trip_id=data.trip_id,
        days=[d.model_dump() for d in data.days]
    )
    db.add(itinerary)
    await db.commit()
    await db.refresh(itinerary)
    return itinerary

async def get_itinerary_by_trip(trip_id: uuid.UUID, user_id: uuid.UUID, db: AsyncSession):

    trips = await db.execute(
        select(Trips).where(Trips.id == trip_id, Trips.user_id == user_id)
    )
    if not trips.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")

    result = await db.execute(
        select(Itineraries).where(Itineraries.trip_id == trip_id)
    )
    return result.scalars().all()