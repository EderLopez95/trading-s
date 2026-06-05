from pydantic import BaseModel
from typing import Any, Optional
from app.domain.enums.enums import StrategyType, SignalType, Timeframe

class Timeframes(BaseModel):
    trend: Timeframe
    entry: Timeframe

class LogEntry(BaseModel):
    level: str
    message: str
    timestamp: str

class SignalResult(BaseModel):
    symbol: Optional[str]
    strategy: Optional[StrategyType]
    timestamp: str
    signal: Optional[SignalType]
    temporality: Optional[Timeframe]
    price: Optional[float]

class MarketData(BaseModel):
    trend: Any
    entry: Any
