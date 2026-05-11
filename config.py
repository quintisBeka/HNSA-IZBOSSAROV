import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///instance/database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN", "BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("CHAT_ID", "CHAT_ID")
    SCAN_TIMEOUT = float(os.getenv("SCAN_TIMEOUT", "0.8"))
