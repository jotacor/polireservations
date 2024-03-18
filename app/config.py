import os
import time


class Config:
    def __init__(self):
        self.debug = os.getenv("DEBUG", False)
        self.start_time = time.time()
        self.login = os.getenv("LOGIN")
        self.home = os.getenv("HOME")
        self.sport = os.getenv("SPORT")
        self.weekday = os.getenv("WEEKDAY") # Miércoles
        self.time = os.getenv("TIME") # 21
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
        self.email = os.getenv("EMAIL")
        self.telegram = os.getenv("TELEGRAM")
        self.credit_number = os.getenv("CREDIT_NUMBER")
        self.credit_expiration = os.getenv("CREDIT_EXPIRATION")
        self.credit_cvc = os.getenv("CREDIT_CVC")
