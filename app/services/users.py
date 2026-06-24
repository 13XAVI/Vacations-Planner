import logging
from fastapi import HTTPException
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import Users
from app.schemas.users import SignupReq, SigningReq
from app.utils.hash import hash_user_password
from app.utils.jwt import create_access_token
from starlette import status

logger = logging.getLogger(__name__)
async def create_new_user(user :SignupReq ,db :AsyncSession):
    try:
        result = await db.execute(select(Users).where(Users.email == user.email))
        user = result.scalar_one_or_none()
        if user :
            raise  HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User is already registered")

        hashed_pass = hash_user_password(user.password)
        new_user = Users(
            username=user.username,
            email=user.email,
            password=hashed_pass
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(str(e))



async  def signIn(credential:SigningReq, db:AsyncSession):
    try:
        result = await  db.execute(
            Select(Users)
            .where(Users.email == credential.email)
        )
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code = 404, detail = "user not found")
        token = create_access_token({"sub":user.email})

        return token
    except HTTPException:
        raise
    except Exception as e:
        logger.error(str(e))


async def get_all_users_db(db: AsyncSession):
    try:
        result = await db.execute(select(Users))
        users = result.scalars().all()
        return  users
    except HTTPException:
        raise
    except Exception as e:
        logger.error(str(e))
