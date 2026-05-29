from plyer import notification

class LocalNotifier:
    def send(self, signal, price, symbol):
        if not signal:
            return

        message = (
            f"Signal: {signal.value}\n"
            f"Price: {price:.2f}"
        )

        notification.notify(
            title=f"Trading Signal for: {symbol}",
            message=message,
            timeout=10
        )
