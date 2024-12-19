from typing import Optional, Dict
from datetime import date
from voith_exercise.repositories.timeseries_repository import TimeseriesRepository
from fastapi import Depends

class TimeseriesService:
    def __init__(self, repository: TimeseriesRepository = Depends()):
        self.repository = repository

    async def get_filtered_data(self, coin_id: str, filters: Dict):
        """
        Get filtered time series data based on provided criteria.
        """
        return await self.repository.fetch_filtered_data(coin_id, filters)

    async def get_summary_stats(self, coin_id: str, start_date: Optional[date], end_date: Optional[date]):
        """
        Get summary statistics for a specific coin within a date range.
        """
        return await self.repository.fetch_summary_stats(coin_id, start_date, end_date)

    async def get_paginated_data(self, coin_id: str, limit: int, offset: int):
        """
        Get paginated time series data for a specific coin.
        """
        return await self.repository.fetch_paginated_data(coin_id, limit, offset)
