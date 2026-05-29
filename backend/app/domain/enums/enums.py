from enum import Enum

class StrategyType(str, Enum):
    MULTI_SMA = "multi_sma"
    RSI_CROSS_TREND = "rsi_cross_trend"

class SignalType(str, Enum):
    SIGNAL = "SIGNAL"
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

class LogType(str, Enum):
    INFO = "INFO"
    ERROR = "ERROR"

class BotStatus(str, Enum):
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"

class ProviderType(str, Enum):
    MT5 = "MT5"
    TRADINGVIEW = "TV"

class Timeframe(str, Enum):
    M5 = "M5"
    M15 = "M15"
    H1 = "H1"
    H4 = "H4"
    D1 = "D1"
    W1 = "W1"
