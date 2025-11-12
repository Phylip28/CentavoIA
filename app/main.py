import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.adapters.api.analysis import analysis_controller
from app.adapters.persistence.database import Base, engine

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Creating tables in the database...")
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Centavo IA Analysis Module",
    description="Analysis Service for Expense Patterns",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(analysis_controller.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Centavo IA Analyssis Service"}
