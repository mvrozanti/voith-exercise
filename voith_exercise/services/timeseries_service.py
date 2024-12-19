from typing import Optional, Dict, List, Any
from datetime import date
from voith_exercise.repositories.timeseries_repository import TimeseriesRepository
from fastapi import Depends, HTTPException, status


class TimeseriesService:
    def __init__(self, repository: TimeseriesRepository = Depends()):
        self.repository = repository

    async def get_filtered_data(self, coin_id: str, filters: Dict) -> List[Dict[str, Any]]:
        if not coin_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coin ID must be provided.",
            )

        try:
            data = await self.repository.fetch_filtered_data(coin_id, filters)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving filtered data: {str(e)}",
            )

        # If no data is returned, just return an empty list instead of raising 404.
        return data if data else []

    async def get_summary_stats(self, coin_id: str, start_date: Optional[date], end_date: Optional[date]) -> Dict[str, Any]:
        """
        Get summary statistics for a specific coin within a date range.
        """
        if not coin_id or not start_date or not end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coin ID, start_date, and end_date must be provided.",
            )

        try:
            stats = await self.repository.fetch_summary_stats(coin_id, start_date, end_date)
            if not stats:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No summary statistics available for coin: {coin_id} in the given date range.",
                )
            return stats
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving summary statistics: {str(e)}",
            )

    async def get_paginated_data(self, coin_id: str, limit: int, offset: int) -> List[Dict[str, Any]]:
        """
        Get paginated time series data for a specific coin.
        """
        if not coin_id or limit <= 0 or offset < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coin ID must be provided, limit must be greater than 0, and offset must be non-negative.",
            )

        try:
            data = await self.repository.fetch_paginated_data(coin_id, limit, offset)
            if not data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No data available for coin: {coin_id} with the given pagination settings.",
                )
            return data
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving paginated data: {str(e)}",
            )
