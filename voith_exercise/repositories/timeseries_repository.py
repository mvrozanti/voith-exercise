from voith_exercise.models.historical_data import HistoricalData
from voith_exercise.db import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, func
from datetime import timedelta
from typing import Dict, Optional, List

class TimeseriesRepository:
    def __init__(self):
        self.db: AsyncSession = SessionLocal()

    async def fetch_filtered_data(self, coin_id: str, filters: Dict) -> List[HistoricalData]:
        """Fetch time series data with filters."""
        conditions = [HistoricalData.coin_id == coin_id]

        # Apply optional filters
        if filters.get("start_date"):
            conditions.append(HistoricalData.timestamp >= filters["start_date"])
        if filters.get("end_date"):
            # Adjust end_date to include the entire day
            adjusted_end_date = filters["end_date"] + timedelta(days=1)
            conditions.append(HistoricalData.timestamp < adjusted_end_date)
        if filters.get("min_price"):
            conditions.append(HistoricalData.price >= filters["min_price"])
        if filters.get("max_price"):
            conditions.append(HistoricalData.price <= filters["max_price"])
        if filters.get("min_volume"):
            conditions.append(HistoricalData.volume >= filters["min_volume"])
        if filters.get("max_volume"):
            conditions.append(HistoricalData.volume <= filters["max_volume"])

        # Build and execute query
        query = select(HistoricalData).where(and_(*conditions))
        result = self.db.execute(query)
        return result.scalars().all()

    async def fetch_summary_stats(self, coin_id: str, start_date: Optional[str], end_date: Optional[str]) -> Dict[str, Optional[float]]:
        """Fetch summary statistics for a specific coin."""
        query = (
            select(
                func.avg(HistoricalData.price).label("avg_price"),
                func.sum(HistoricalData.volume).label("total_volume"),
            )
            .where(
                HistoricalData.coin_id == coin_id,
                HistoricalData.timestamp >= start_date,
                HistoricalData.timestamp <= end_date,
            )
        )
        result = self.db.execute(query)
        stats = result.fetchone()
        return {
            "avg_price": stats.avg_price if stats else None,
            "total_volume": stats.total_volume if stats else None,
        } if stats else {}

    async def fetch_paginated_data(self, coin_id: str, limit: int, offset: int) -> List[HistoricalData]:
        """Fetch paginated time series data."""
        query = (
            select(HistoricalData)
            .where(HistoricalData.coin_id == coin_id)
            .order_by(HistoricalData.timestamp)
            .limit(limit)
            .offset(offset)
        )
        result = self.db.execute(query)
        return result.scalars().all()
