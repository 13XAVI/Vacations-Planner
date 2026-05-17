import uuid
from typing import List
from pydantic import BaseModel

class DayPlan(BaseModel):
    day: int
    activities: List[str]

class itinerary_req(BaseModel):
    trip_id: uuid.UUID
    days: List[DayPlan]

class itinerary_res(BaseModel):
    trip_id: uuid.UUID
    itinerary: List[DayPlan]
    message: str = "Itinerary created successfully"

    class Config:
        from_attributes = True