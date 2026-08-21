import uuid
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class SignupReq(BaseModel):
    username:str = Field(min_length=3,description="username should have minimum 3 character ")
    email:EmailStr
    password:str = Field(min_length=6,description="password need minimum 6 characters")

class SigningReq(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6,description="password need minimum 6 characters")

class SigningToken(BaseModel):
    token:str

class UpdateUserReq(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class SignupRes(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str
    class Config:
        from_attributes = True
