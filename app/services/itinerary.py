import logging
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.llm.chatbot import generate_itineraries
from app.models.trips import Trips
from app.models.itinerary import Itineraries
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)


async def create_itinerary(trip_id: uuid.UUID, user_id: uuid.UUID, db: AsyncSession):
    result = await db.execute(
        select(Trips).where(Trips.id == trip_id, Trips.user_id == user_id)
    )
    trip = result.scalar_one_or_none()
    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")

    itinerary_days = generate_itineraries(
        destination=trip.destination,
        days=trip.days,
        budget=trip.budget,
        travel_style=trip.trip_style
    )
    itinerary = await db.execute(select(Itineraries).where(Itineraries.trip_id == trip_id))
    existing_itinerary = itinerary.scalar_one_or_none()

    if existing_itinerary:
        existing_itinerary.days = itinerary_days
        await db.commit()
        await db.refresh(existing_itinerary)
        return existing_itinerary

    new_itinerary = Itineraries(
        trip_id=trip_id,
        days=itinerary_days
    )
    db.add(new_itinerary)
    await db.commit()
    await db.refresh(new_itinerary)
    return new_itinerary


async def get_itinerary_by_trip(trip_id: uuid.UUID, user_id: uuid.UUID, db: AsyncSession):
    trips = await db.execute(
        select(Trips).where(Trips.id == trip_id, Trips.user_id == user_id)
    )
    if not trips.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Itinerary not found")

    result = await db.execute(
        select(Itineraries).where(Itineraries.trip_id == trip_id)
    )
    return result.scalars().all()
