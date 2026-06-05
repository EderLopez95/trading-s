from plyer import notification

class LocalNotifier:
    def send(self, signal, symbol):
        if not signal:
            return

        notification.notify(
            title=f"SIGNAL FOR: {symbol}",
            message=f"{signal.value}",
            timeout=10
        )
