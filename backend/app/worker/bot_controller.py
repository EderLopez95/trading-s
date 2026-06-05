import threading
from app.worker.bot_runner import BotRunner
from app.domain.exceptions import BotAlreadyRunningError, BotNotRunningError
from app.domain.enums.enums import BotStatus

class BotController:
    def __init__(self):
        self.bot = BotRunner()
        self.thread = None

    def start(self):
        try:
            if self.thread and self.thread.is_alive():
                raise BotAlreadyRunningError("Bot is already running")
            
            self.thread = threading.Thread(target=self.bot.start)
            self.thread.daemon = True
            self.thread.start()
            return BotStatus.RUNNING.value
        except Exception:
            raise

    def stop(self):
        try:
            if not self.bot or not self.thread or not self.thread.is_alive():
                raise BotNotRunningError("Bot is not running")
            
            self.bot.stop()
            return BotStatus.STOPPED.value
        except Exception:
            raise

    def status(self):
        if self.thread and self.thread.is_alive():
            return BotStatus.RUNNING.value
        return BotStatus.STOPPED.value
