from datetime import datetime, timezone
from app.domain.services.strategy_engine import StrategyEngine
from app.domain.models.models import SignalResult, MarketData
from app.domain.models.config_model import ConfigModel

class AnalyzeMarket:
    def __init__(self, provider):
        self.provider = provider
        self.engine = StrategyEngine()

    def execute(self, symbol, config: ConfigModel) -> SignalResult:
        # fetch market data from provider for specific symbol and timeframes defined in config
        data = MarketData(
            trend = self.provider.get_data(symbol, config.timeframes.trend),
            entry = self.provider.get_data(symbol, config.timeframes.entry, 50) # minimum data required
        )
        signal, logs = self.engine.run(config.strategy, data)

        return SignalResult(
            symbol = symbol,
            strategy = config.strategy,
            timestamp = datetime.now(timezone.utc).isoformat(),
            signal = signal,
            temporality = config.timeframes.trend,
            price = data.entry["close"].iloc[-1], # get price from open candle
            logs = logs
        )
