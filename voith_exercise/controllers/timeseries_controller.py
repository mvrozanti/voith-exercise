from fastapi import APIRouter, Depends, Query, HTTPException
from voith_exercise.services.timeseries_service import TimeseriesService
from typing import Optional, List
from datetime import date

router = APIRouter()

@router.get("/timeseries/coins", response_model=List[str], summary="Get all distinct coins", tags=["Time Series"])
async def get_all_coins(service: TimeseriesService = Depends(TimeseriesService)):
    """
    Returns a list of all distinct coin IDs available in the database.
    """
    return await service.get_all_coins()


@router.get("/timeseries/{coin_id}")
async def get_data(
    coin_id: str,
    start_date: Optional[date] = Query(None, description="Filter from this date"),
    end_date: Optional[date] = Query(None, description="Filter up to this date"),
    min_price: Optional[float] = Query(None, description="Filter by minimum price"),
    max_price: Optional[float] = Query(None, description="Filter by maximum price"),
    min_volume: Optional[float] = Query(None, description="Filter by minimum volume"),
    max_volume: Optional[float] = Query(None, description="Filter by maximum volume"),
    service: TimeseriesService = Depends(TimeseriesService),
):
    filters = {
        "start_date": start_date,
        "end_date": end_date,
        "min_price": min_price,
        "max_price": max_price,
        "min_volume": min_volume,
        "max_volume": max_volume,
    }
    data = await service.get_filtered_data(coin_id, filters)
    if not data["timestamps"]:
        raise HTTPException(status_code=404, detail="No data found for the given criteria")
    return {"coin_id": coin_id, **data}

@router.get("/timeseries/{coin_id}/stats")
async def get_stats(
    coin_id: str,
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    service: TimeseriesService = Depends(TimeseriesService),
):
    """
    Get summary statistics (e.g., average price, total volume) for a coin within a date range.
    """
    stats = await service.get_summary_stats(coin_id, start_date, end_date)
    if not stats["summary"]:
        raise HTTPException(status_code=404, detail="No data found for the given criteria")
    return {"coin_id": coin_id, "stats": stats["summary"]}


@router.get("/timeseries/{coin_id}/paginated")
async def get_paginated_data(
    coin_id: str,
    limit: int = Query(10, description="Number of results to return, must be > 0"),
    offset: int = Query(0, description="Number of results to skip, must be >= 0"),
    service: TimeseriesService = Depends(TimeseriesService),
):
    """
    Get paginated time series data for a specific coin.
    """
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be greater than 0.")
    if offset < 0:
        raise HTTPException(status_code=400, detail="Offset must be non-negative.")

    data = await service.get_paginated_data(coin_id, limit, offset)

    if not data["timestamps"]:
        raise HTTPException(status_code=404, detail="No data found for the given criteria")

    return data
