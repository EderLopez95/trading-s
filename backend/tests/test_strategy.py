from app.infrastructure.data_provider.mt5_provider import MT5Provider
from app.infrastructure.config.config_loader import load_config
from app.application.use_cases.analyze_market import AnalyzeMarket

provider = MT5Provider()
config = load_config()

analyzer = AnalyzeMarket(provider)

result = analyzer.execute("F", config)

print(result)
