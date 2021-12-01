import os

class Config(object):
    API_HASH = os.getenv("API_HASH")
    API_ID = int(os.getenv("API_ID"))
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL"))
