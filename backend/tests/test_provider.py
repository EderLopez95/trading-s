from app.infrastructure.data_provider.mt5_provider import MT5Provider

provider = MT5Provider()

df = provider.get_data("AAPL", "M5")

print(df.tail())
