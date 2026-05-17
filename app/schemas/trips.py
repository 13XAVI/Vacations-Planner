import uuid
from pydantic import BaseModel

class trip_req(BaseModel):
    destination: str
    days: int
    budget: float
    trip_style: str

class trip_res(BaseModel):
    id: uuid.UUID
    destination: str
    days: int
    budget: float
    trip_style: str
    message: str = "Trip created successfully"

    class Config:
        from_attributes = True