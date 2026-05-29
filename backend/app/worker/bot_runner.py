from datetime import datetime, timezone
import threading
from app.infrastructure.config.config_loader import load_config
from app.infrastructure.data_provider.mt5_provider import MT5Provider
from app.application.use_cases.analyze_market import AnalyzeMarket
from app.infrastructure.ws.ws_manager import ws_manager
from app.domain.enums.enums import LogType, SignalType
from app.domain.models.models import LogWSMessage, SignalResult, LogEntry
from app.infrastructure.notifications.local_notifier import LocalNotifier

class BotRunner:
    def __init__(self):
        self.running = False
        self.stop_event = threading.Event()
        self.provider = MT5Provider()
        self.analyzer = AnalyzeMarket(self.provider)
        self.notifier = LocalNotifier()
        self.last_signal_candle = {}

    def _send_signal(self, type, signal: SignalResult):
        self._send_ws(
            LogWSMessage(
                type = type,
                data = signal
            )
        )

    def _send_ws(self, message):
        ws_manager.send(message.model_dump())

    def start(self):
        self.running = True
        self.stop_event.clear()

        while self.running:
            try:
                config = load_config()
                symbols = config.symbols
                interval = max(10, config.execution_interval) # ensure minimum interval of 10 seconds to prevent overload
                
                if len(symbols) == 0:
                    self._send_ws(LogEntry(
                        level = LogType.INFO.value,
                        message = "No symbols configured, skipping cycle.",
                        timestamp = datetime.now(timezone.utc).isoformat()
                    ))
                else:
                    for symbol in config.symbols:
                        try:
                            # get trend data
                            df_trend = self.provider.get_data(symbol, config.timeframes.trend)
                            # execute analysis and strategy
                            result = self.analyzer.execute(symbol, config)
                            # in case of logs or signals, send to ws and notifier
                            if result.logs:
                                for log in result.logs:
                                    self._send_ws(log)
                            if result.signal != SignalType.HOLD.value:
                                # send signal only if it is a new candle to prevent duplicates
                                candle_time = df_trend.index[-1]
                                last_candle = self.last_signal_candle.get(symbol)
                                if last_candle == candle_time:
                                    continue
                                self.last_signal_candle[symbol] = candle_time
                                self.notifier.send(result.signal, result.price, symbol)
                                self._send_signal(SignalType.SIGNAL.value, result)
                        except Exception as e:
                            self._send_ws(LogEntry(
                                level = LogType.ERROR.value,
                                message = f"Error processing symbol {symbol}: {str(e)}",
                                timestamp = datetime.now(timezone.utc).isoformat()
                            ))
                            
                if self.stop_event.wait(timeout=interval):
                    break

            except Exception as e:
                self._send_ws(LogEntry(
                    level = LogType.ERROR.value,
                    message = f"Error in bot runner: {str(e)}",
                    timestamp = datetime.now(timezone.utc).isoformat()
                ))

    def stop(self):
        self.running = False
        self.stop_event.set()
