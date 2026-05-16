from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routes_deps import get_current_user, require_admin
from app.core.lifespan_db import create_session
from app.models.users import Users
from app.schemas.users import signup_res
from app.services.users import get_all_users_db

router = APIRouter(
    prefix="/users",
    tags=["user"]
)


@router.get("/all_users", status_code=HTTPStatus.OK, response_model=List[signup_res])
async def get_all_users( session: AsyncSession = Depends(create_session),_: Users = Depends(require_admin)  ):
    return await get_all_users_db(session)

@router.get("/me", status_code=HTTPStatus.OK, response_model=signup_res)
async def get_me(current_user: Users = Depends(get_current_user)):
    return current_user