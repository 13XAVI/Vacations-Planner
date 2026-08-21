import uuid
from typing import List
from pydantic import BaseModel, ConfigDict, Field

class DayPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")
    day: int
    activities: list[str]
class ItineraryReq(BaseModel):
    trip_id: uuid.UUID
    days: List[DayPlan]

class ItineraryContent(BaseModel):
    model_config = ConfigDict(extra="forbid")
    itinerary: List[DayPlan]
    estimated_cost: float | None = None
    accommodation: str | None = None
    notes: str | None = None
    message: str = "Itinerary created successfully"


class ItineraryRes(ItineraryContent):
    trip_id: uuid.UUID