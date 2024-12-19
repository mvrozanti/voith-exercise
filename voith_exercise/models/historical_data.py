from sqlalchemy import Column, String, DateTime, Float
from voith_exercise.db import Base

class HistoricalData(Base):
    __tablename__ = "historical_data"

    coin_id = Column(String(50), primary_key=True)
    timestamp = Column(DateTime, primary_key=True)
    price = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)