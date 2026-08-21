import uuid
from http import HTTPStatus
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.routes_deps import get_current_user
from app.core.lifespan_db import create_session
from app.models.users import Users
from app.schemas.itinerary import ItineraryReq
from app.services.itinerary import create_itinerary, get_itinerary_by_trip

router = APIRouter(prefix="/itineraries", tags=["itineraries"])

@router.post("", status_code=HTTPStatus.CREATED)
async def create(
    trip_id: uuid.UUID,
    current_user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(create_session)
):
    itinerary = await create_itinerary(trip_id, current_user.id, session)
    return {
        "trip_id": itinerary.trip_id,
        "itinerary": itinerary.days,
        "message": "Itinerary created successfully"
    }

@router.get("/{trip_id}", status_code=HTTPStatus.OK)
async def get_by_trip(
    trip_id: uuid.UUID,
    current_user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(create_session)
):
    return await get_itinerary_by_trip(trip_id, current_user.id, session)