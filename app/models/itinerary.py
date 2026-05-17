import uuid
from sqlalchemy import Column, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.base import Base

class Itineraries(Base):
    __tablename__ = "itineraries"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_id = Column(UUID(as_uuid=True), ForeignKey("trips.id"), nullable=False)
    days = Column(JSON, nullable=False)
    trip = relationship("Trips", back_populates="itineraries")