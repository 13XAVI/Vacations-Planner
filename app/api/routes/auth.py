from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.lifespan_db import create_session
from app.schemas.users import SignupRes, SigningReq, SigningToken
from app.services.users import create_new_user, signIn

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register", status_code=HTTPStatus.CREATED, response_model=SignupRes, tags=["auth"])
async def create_user(user: SignupRes, session: AsyncSession = Depends(create_session)):
    return await  create_new_user(user, session)

@router.post("/signin",status_code = HTTPStatus.OK,response_model = SigningToken, tags=["auth"])
async  def sign_in_user(user:SigningReq ,session:AsyncSession = Depends(create_session)):
     token = await  signIn(user,session)
     return {"token":token}
