from voith_exercise.models.historical_data import HistoricalData
from voith_exercise.db import SessionLocal

class TimeseriesRepository:
    def __init__(self):
        self.db = SessionLocal()

    async def fetch_data_by_coin_id(self, coin_id: str):
        return self.db.query(HistoricalData).filter(HistoricalData.coin_id == coin_id).all()
