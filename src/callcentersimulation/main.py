from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.callcentersimulation.infrastructure.api.endpoints.tickets import router as tickets_router
from src.callcentersimulation.infrastructure.persistence.conf.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connection pool is managed automatically
    yield
    await engine.dispose()

app = FastAPI(
    title="Call Center simulator",
    description="API for uploading and processing call center tickets with hexagonal architecture",
    version="1.0.0"
)

app.include_router(tickets_router)

