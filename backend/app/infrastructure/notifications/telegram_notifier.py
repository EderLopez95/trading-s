import requests
from app.infrastructure.config.settings import settings
from datetime import datetime, timezone

class TelegramNotifier:
    def __init__(self):
        self.token = settings.telegram_token
        self.chat_id = settings.telegram_chat_id
        self.now = datetime.now(timezone.utc)

    def send(self, signal, symbol, temporality, strategy, price=0):
        message = (
            f"Stock: <b>{symbol}</b>\n"
            f"Signal: <b>{signal.value}</b>\n"
            f"Temp: <b>{temporality.value}</b>\n"
            f"Strategy: <b>{strategy.value}</b>\n"
            f"Price: {price:.2f}\n"
            f"Time: {int(self.now.strftime('%I'))}:{self.now.strftime('%M%p %d/%m/%y')}"
        )

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"

        try:
            response = requests.post(url, json={
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML"
            })
            # properly handle response status to propagate errors if any
            response.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"Telegram Notifier error: {str(e)}")
