from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from kabeer import kabeercmd

START_MESSAGE = (
        'Hello there[!](https://telegra.ph/file/25b9742e3ca755306cd94.png)\n'
        'I can generate session of [pyrogram](https://t.me/pyrogram) and [telethon](https://t.me/TelethonUpdates).\n\n'
        '**Note:** We are not responsible for any harm, And we do not collect your credentials.\n'
        'By [Miss Akshi Official](https://t.me/Miss_Akshi_updates)'
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
