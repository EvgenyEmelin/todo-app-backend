from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.category import router_category
from app.api.routers.task import router as task_router
from app.db.session import engine
from app.models.base import Base


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router=task_router)
app.include_router(router=router_category)

app.add_middleware(
    CORSMiddleware,
    allow_methods=["*"],
    allow_origins=["http://localhost:3000"],
    allow_headers=["*"])

