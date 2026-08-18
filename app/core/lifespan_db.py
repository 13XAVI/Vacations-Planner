from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.core.config import settings
from app.core.base import Base
from app.models.users import Users
from app.models.trips import Trips
from app.models.itinerary import Itineraries

engine =  create_async_engine(settings.DATA_BASE_URL)
session_maker = async_sessionmaker(engine,expire_on_commit=False)


async def create_db_tables():
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)

async def create_session():
    async with session_maker() as session:
        yield session