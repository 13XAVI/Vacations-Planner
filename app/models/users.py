import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime
from app.core.base import Base


class Users(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    username= Column(String,nullable=False)
    email=Column(String,nullable=False)
    password = Column(String,nullable=False)
    role=Column(String,default="user")
