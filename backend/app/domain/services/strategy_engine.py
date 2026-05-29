from datetime import datetime, timezone
from app.domain.strategies.multi_sma_strategy import MultiSMAStrategy
from app.domain.strategies.rsi_cross_trend_strategy import RSICrossTrendStrategy
from app.domain.enums.enums import StrategyType, SignalType, LogType
from app.domain.models.models import LogEntry

class StrategyEngine:
    def __init__(self):
        # add strategies from strategies folder, they must implement an execute method that returns a signal
        self.strategies = {
            StrategyType.MULTI_SMA.value: MultiSMAStrategy(),
            StrategyType.RSI_CROSS_TREND.value: RSICrossTrendStrategy()
        }
        self.default_strategy = StrategyType.MULTI_SMA.value

    def _add_log(self, logs, level, message):
        logs.append(LogEntry(
            level = level,
            message = message,
            timestamp = datetime.now(timezone.utc).isoformat()
        ))

    def run(self, strategy_name, data):
        strategy = self.strategies.get(strategy_name)
        logs = []
        
        if strategy is None:
            self._add_log(logs, LogType.INFO.value, f"Strategy '{strategy_name}' not found. Using default '{self.default_strategy}'")
            strategy = self.strategies[self.default_strategy]

        try:
            signal = strategy.execute(data)
            if signal not in [SignalType.BUY.value, SignalType.SELL.value, SignalType.HOLD.value]:
                self._add_log(logs, LogType.INFO.value, f"Invalid signal '{signal}', defaulting to HOLD")
                return SignalType.HOLD.value, logs
            return signal, logs
        except Exception as e:
            self._add_log(logs, LogType.ERROR.value, f"Error executing strategy '{strategy_name}': {e}")
            return SignalType.HOLD.value, logs
