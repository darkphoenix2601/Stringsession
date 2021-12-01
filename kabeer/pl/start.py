from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from kabeer import kabeercmd

START_MESSAGE = (
        'Hello there[!](https://telegra.ph/file/e677cf0a08017d8ca0915.jpg)\n'
        'I can generate session of [pyrogram](https://t.me/pyrogram) and [telethon](https://t.me/TelethonUpdates).\n\n'
        '**Note:** We are not responsible for any harm, And we do not collect your credentials.\n'
        'By [RhythmOfficial](https://t.me/RhythmOfficial)'
    )

KEYBOARD = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text='Pyrogram', callback_data='sele_pyrogram')],
    [InlineKeyboardButton(text='Telethon', callback_data='sele_telethon')]]
)

@kabeercmd.on_message(filters.command('start'))
async def start(sessionCli, message):
    await message.reply(
        text=START_MESSAGE,
        reply_markup=KEYBOARD,
        disable_web_page_preview=False
    )
