from typing import Optional, Dict, List, Any
from datetime import date
from voith_exercise.repositories.timeseries_repository import TimeseriesRepository
from fastapi import Depends
import logging

logger = logging.getLogger(__name__)

class TimeseriesService:
    def __init__(self, repository: TimeseriesRepository = Depends()):
        self.repository = repository

    async def get_filtered_data(self, coin_id: str, filters: Dict) -> Dict[str, List]:
        return await self.repository.fetch_filtered_data(coin_id, filters)

    async def get_summary_stats(
        self, coin_id: str, start_date: Optional[date], end_date: Optional[date]
    ) -> Dict[str, Any]:
        """Get summary statistics for a specific coin within a date range."""
        if not coin_id or not start_date or not end_date:
            logger.warning("Invalid parameters for get_summary_stats")
            raise ValueError("Coin ID, start_date, and end_date must be provided.")

        logger.info(f"Fetching summary stats for coin_id={coin_id} from {start_date} to {end_date}")
        stats = await self.repository.fetch_summary_stats(coin_id, start_date, end_date)

        if not stats or not stats["avg_price"]:
            logger.warning(f"No stats found for coin_id={coin_id}")
            return {"summary": None}

        return {"summary": stats}

    async def get_paginated_data(self, coin_id: str, limit: int, offset: int) -> Dict[str, Any]:
        """Get paginated time series data for a specific coin."""
        if not coin_id or limit <= 0 or offset < 0:
            logger.warning("Invalid pagination parameters for get_paginated_data")
            raise ValueError("Coin ID must be provided, limit > 0, and offset >= 0.")

        logger.info(f"Fetching paginated data for coin_id={coin_id}, limit={limit}, offset={offset}")
        data = await self.repository.fetch_paginated_data(coin_id, limit, offset)

        # Transform the result into the optimized format
        timestamps = [row.timestamp for row in data]
        prices = [row.price for row in data]
        volumes = [row.volume for row in data]

        return {
            "coin_id": coin_id,
            "timestamps": timestamps,
            "prices": prices,
            "volumes": volumes,
        }
