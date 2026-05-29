from app.domain.enums.enums import SignalType
from app.domain.strategies.utils import Utils
from app.domain.models.models import MarketData

class MultiSMAStrategy:
    def __init__(self):
        self.utils = Utils()

    def execute(self, data: MarketData):
        # data from provider
        df_trend = data.trend
        df_entry = data.entry

        # calculate SMAs
        sma20 = df_trend["close"].rolling(20).mean()
        sma40 = df_trend["close"].rolling(40).mean()
        sma100 = df_trend["close"].rolling(100).mean()
        sma200 = df_trend["close"].rolling(200).mean()
        sma20_v = sma20.iloc[-1]
        sma40_v = sma40.iloc[-1]
        sma100_v = sma100.iloc[-1]
        sma200_v = sma200.iloc[-1]

        # determine trend based on SMA order
        bullish_trend = sma20_v > sma40_v > sma100_v > sma200_v
        bearish_trend = sma20_v < sma40_v < sma100_v < sma200_v

        # calculate RSI
        rsi = self.utils.calculate_rsi(df_entry["close"], 14)
        rsi_ma = rsi.rolling(14).mean()
        bullish_cross = self.utils.crossover(rsi, rsi_ma)
        bearish_cross = self.utils.crossunder(rsi, rsi_ma)
        
        # calculate volume
        volume_avg = df_entry["tick_volume"].rolling(20).mean()
        volume_v = df_entry.iloc[-1]["tick_volume"]
        volume_avg_v = volume_avg.iloc[-1]
        volume_ok = volume_v > volume_avg_v
        
        if bullish_trend and bullish_cross and volume_ok:
            return SignalType.BUY.value

        if bearish_trend and bearish_cross and volume_ok:
            return SignalType.SELL.value

        return SignalType.HOLD.value
