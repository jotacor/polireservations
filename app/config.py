import os
import time


class Config:
    def __init__(self):
        self.debug = bool(os.getenv("DEBUG", False))
        self.selenium = os.getenv("SELENIUM", "http://localhost:4444")
        self.start_time = time.time()
        self.login = os.getenv("LOGIN")
        self.home = os.getenv("HOME")
        self.sport = os.getenv("SPORT")
        self.weekday = os.getenv("WEEKDAY") # Miércoles
        self.time = os.getenv("TIME") # 21
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
        self.email = os.getenv("EMAIL")
        self.credit_number = os.getenv("CREDIT_NUMBER")
        self.credit_expiration = os.getenv("CREDIT_EXPIRATION")
        self.credit_cvc = os.getenv("CREDIT_CVC")
        self.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID", None)
        self.telegram_token = os.getenv("TELEGRAM_TOKEN", None)