import uuid
from typing import List
from pydantic import BaseModel, Field


class DayPlan(BaseModel):
    day: int = Field(ge=1)
    activities: List[str] = Field(
        min_length=1,
        description="List of trip activities"
    )

class ItineraryReq(BaseModel):
    trip_id: uuid.UUID
    days: List[DayPlan]

class ItineraryRes(BaseModel):
    trip_id: uuid.UUID
    itinerary: List[DayPlan]
    message: str = "Itinerary created successfully"

    class Config:
        from_attributes = True