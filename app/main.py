import logging
import uvicorn
from contextlib import asynccontextmanager
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as user_router
from fastapi import FastAPI

from app.api.routes_deps import logging_middleware
from app.core.lifespan_db import create_db_tables

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(name)s | %(message)s"
)

@asynccontextmanager
async def lifespan_db(app:FastAPI):
    await  create_db_tables()
    yield

app = FastAPI(
    title="Vacation Planning",
    lifespan=lifespan_db,
    version="1.0",
    summary= """
    Vacation Planning is a backend REST API built with FastAPI that helps users
    organize and manage their trips efficiently.
    """)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)
app.include_router(auth_router)
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app",host="127.0.0.1",port=8080,reload=True)