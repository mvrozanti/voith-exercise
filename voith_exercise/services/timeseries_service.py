from typing import Optional, Dict, List, Any
from datetime import date
from voith_exercise.repositories.timeseries_repository import TimeseriesRepository
from fastapi import Depends
import logging

logger = logging.getLogger(__name__)

class TimeseriesService:
    def __init__(self, repository: TimeseriesRepository = Depends()):
        self.repository = repository

    async def get_filtered_data(self, coin_id: str, filters: Dict) -> List[Dict[str, Any]]:
        if not coin_id:
            logger.warning("Missing coin_id in get_filtered_data")
            raise ValueError("Coin ID must be provided.")

        logger.info(f"Fetching filtered data for coin_id={coin_id} with filters={filters}")
        try:
            data = await self.repository.fetch_filtered_data(coin_id, filters)
            return data if data else []
        except Exception as e:
            logger.error(f"Error retrieving filtered data: {e}")
            raise RuntimeError(f"Failed to fetch filtered data for coin_id={coin_id}")

    async def get_summary_stats(self, coin_id: str, start_date: Optional[date], end_date: Optional[date]) -> Dict[str, Any]:
        if not coin_id or not start_date or not end_date:
            logger.warning("Invalid parameters for get_summary_stats")
            raise ValueError("Coin ID, start_date, and end_date must be provided.")

        logger.info(f"Fetching summary stats for coin_id={coin_id} from {start_date} to {end_date}")
        try:
            stats = await self.repository.fetch_summary_stats(coin_id, start_date, end_date)
            return stats if stats else {}
        except Exception as e:
            logger.error(f"Error retrieving summary stats: {e}")
            raise RuntimeError(f"Failed to fetch summary stats for coin_id={coin_id}")

    async def get_paginated_data(self, coin_id: str, limit: int, offset: int) -> List[Dict[str, Any]]:
        if not coin_id or limit <= 0 or offset < 0:
            logger.warning("Invalid pagination parameters for get_paginated_data")
            raise ValueError("Coin ID must be provided, limit > 0, and offset >= 0.")

        logger.info(f"Fetching paginated data for coin_id={coin_id}, limit={limit}, offset={offset}")
        try:
            data = await self.repository.fetch_paginated_data(coin_id, limit, offset)
            return data if data else []
        except Exception as e:
            logger.error(f"Error retrieving paginated data: {e}")
            raise RuntimeError(f"Failed to fetch paginated data for coin_id={coin_id}")
