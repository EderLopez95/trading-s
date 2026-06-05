import os

dotenv_loaded = False

# load environment variables from .env file if available, otherwise rely on system environment variables
try:
    from dotenv import load_dotenv
    
    if os.path.exists(".env.local"):
        load_dotenv(".env.local")
        dotenv_loaded = True
    elif os.path.exists(".env"):
        load_dotenv(".env")
        dotenv_loaded = True
except ImportError:
    dotenv_loaded = False

class Settings:
    def __init__(self):
        self.env = os.getenv("ENV", "development")
        self.telegram_token = os.getenv("TELEGRAM_TOKEN")
        self.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self._validate()

    def _validate(self):
        if not self.telegram_token:
            raise ValueError("Missing TELEGRAM_TOKEN")

        if not self.telegram_chat_id:
            raise ValueError("Missing TELEGRAM_CHAT_ID")

settings = Settings()
