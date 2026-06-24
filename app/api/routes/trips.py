import uuid
from http import HTTPStatus
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from app.api.routes_deps import get_current_user, require_admin
from app.core.lifespan_db import create_session
from app.models.users import Users
from app.schemas.trips import TripReq, TripRes
from app.services.trips import create_trip, get_all_trips, get_trip_by_id, update_trip, delete_trip

router = APIRouter(prefix="/trips", tags=["trips"])

@router.post("", status_code=HTTPStatus.CREATED, response_model=TripRes)
async def create(
    data: TripReq,
    current_user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(create_session)
):
    trip =  await create_trip(data, current_user.id, session)
    return TripRes(
        id = trip.id,
        destination=trip.destination,
        days=trip.days,
        budget=trip.budget,
        trip_style=trip.trip_style,
        message="Trip successfully Created"
    )

@router.get("", status_code=HTTPStatus.OK, response_model=List[TripRes])
async def get_all(
    current_user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(create_session)
):
    return await get_all_trips(current_user.id, session)

@router.get("/{trip_id}", status_code=HTTPStatus.OK, response_model=TripRes)
async def get_one(
    trip_id: uuid.UUID,
    current_user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(create_session)
):
    return await get_trip_by_id(trip_id, current_user.id, session)

@router.put("/{trip_id}", status_code=HTTPStatus.OK, response_model=TripRes)
async def update(
    trip_id: uuid.UUID,
    data: TripReq,
    current_user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(create_session)
):
    trip =  await update_trip(trip_id, data, current_user.id, session)
    return TripRes(
        id=trip.id,
        destination=trip.destination,
        days=trip.days,
        budget=trip.budget,
        trip_style=trip.trip_style,
        message="Trip successfully updated"
    )

@router.delete("/{trip_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete(
    trip_id: uuid.UUID,
    current_user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(create_session),
    _: Users = Depends(require_admin)
):
    await delete_trip(trip_id, current_user.id, session)