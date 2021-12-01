from pyrogram import Client
from pyromod import listen
from kabeer.config import Config


# Init bot session
API_ID = Config.API_ID
API_HASH = Config.API_HASH
BOT_TOKEN = Config.BOT_TOKEN
LOG_CHANNEL = Config.LOG_CHANNEL

kabeercmd = Client(
    'botSession',
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(
        root='kabeer.pl'
    )
)
print("Started")
