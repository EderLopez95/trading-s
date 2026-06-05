from enum import Enum

class StrategyType(str, Enum):
    RSI_CROSS_TREND = "rsi_cross_trend"
    MULTI_SMA = "multi_sma"

class StrategyNameType(str, Enum):
    RSI_CROSS_TREND_value = "RSI 14 Cross Trend"
    MULTI_SMA_value = "Multi SMA (20,40,100,200) + Cross RSI 14 + Tick Volume"

class SignalType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

class LogType(str, Enum):
    INFO = "INFO"
    ERROR = "ERROR"

class BotStatus(str, Enum):
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"

class Timeframe(str, Enum):
    M5 = "M5"
    M15 = "M15"
    H1 = "H1"
    H4 = "H4"
    D1 = "D1"
    W1 = "W1"
