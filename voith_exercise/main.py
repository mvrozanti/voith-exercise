from fastapi import FastAPI
from voith_exercise.controllers.timeseries_controller import router as data_router
from voith_exercise.db import Base, engine

app = FastAPI(
    title="Voith Exercise - Timeseries API",
    description="An API for querying and managing cryptocoin time series data",
    version="0.1.0",
)

Base.metadata.create_all(bind=engine)

app.include_router(data_router, prefix="/api/v1/data", tags=["Data"])

@app.get("/health", tags=["Health"])
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}
