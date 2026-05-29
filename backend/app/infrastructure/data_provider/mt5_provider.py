import MetaTrader5 as mt5
import pandas as pd

class MT5Provider:
    def __init__(self):
        self.TIMEFRAME_MAP = {
            "M5": mt5.TIMEFRAME_M5,
            "M15": mt5.TIMEFRAME_M15,
            "H1": mt5.TIMEFRAME_H1,
            "H4": mt5.TIMEFRAME_H4,
            "D1": mt5.TIMEFRAME_D1,
            "W1": mt5.TIMEFRAME_W1,
        }
        if not mt5.initialize():
            raise Exception(f"MT5 init error: {mt5.last_error()}")

    def get_data(self, symbol, timeframe, n=100):
        tf = self.TIMEFRAME_MAP[timeframe]
        rates = mt5.copy_rates_from_pos(symbol, tf, 0, n)
        if rates is None:
            raise Exception(f"No data for {symbol}")
        df = pd.DataFrame(rates)
        return df

    def search_symbols(self, query: str = ""):
        query = query.upper()
        symbols = mt5.symbols_get()
        # prioritize symbols that start with the query and have less characters, then symbols that contain the query
        starts_with = [
            s.name for s in symbols
            if s.name.upper().startswith(query)
        ]
        contains = [
            s.name for s in symbols
            if query in s.name.upper() and s.name not in starts_with
        ]
        result = starts_with + contains
        result = sorted(
            result,
            key=lambda x: (not x.startswith(query), len(x))
        )
        return result[:20]
