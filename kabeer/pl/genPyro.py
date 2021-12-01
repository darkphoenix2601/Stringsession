from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

from pyrogram.errors.exceptions import bad_request_400
from pyrogram.errors import (
    FloodWait,
    SessionPasswordNeeded,
    PhoneCodeInvalid,
    PhoneCodeExpired
)

from kabeer import (
    kabeercmd,
    LOG_CHANNEL
)

async def pyroCreateSession(api_id: int, api_hash: str):
    return Client(":memory:", api_id=int(api_id), api_hash=str(api_hash)) 

@kabeercmd.on_callback_query(filters.create(lambda _, __, query: 'sele_pyrogram' in query.data))
async def pyroGen(kabeercmd, callback_data):
    user_id = callback_data.from_user.id
    
    await kabeercmd.delete_messages(
        user_id,
        callback_data.message.message_id
    )

    # Init the process to get `API_ID`
    API_ID = await kabeercmd.ask(
        chat_id=user_id,
        text=(
            'Send me your `API_ID` you can find it on my.telegram.org after you logged in.'
        )
    )
    if not (
        API_ID.text.isdigit()
    ):
        await kabeercmd.send_message(
            chat_id=user_id,
            text='API_ID should be integer and valid in range limit.'
        )
        return
    
    # Init the process to get `API_HASH`
    API_HASH = await kabeercmd.ask(
        chat_id=user_id,
        text=(
            'Send me your `API_HASH` you can find it on my.telegram.org after you logged in.'
        )
    )
    
    # Init the prcess to get phone number.
    PHONE = await kabeercmd.ask(
        chat_id=user_id,
        text=(
            'Now send me your `phone number` in international format or your `bot_token`'
        )
    )    
    if str(PHONE.text).startswith('+'):
        
        # Creating userClient 
        try:
            userClient = await pyroCreateSession(int(API_ID.text), str(API_HASH.text))
        except Exception as e:
            await API_HASH.reply(f'**Something went wrong**:\n`{e}`')
            return
        
        try:
            await userClient.connect()
        except ConnectionError:
            await userClient.disconnect()
            await userClient.connect()
        
        try:
            sent_code = await userClient.send_code(PHONE.text)
        except FloodWait as e:
            await kabeercmd.send_message(
                chat_id=user_id,
                text=(
                    f"I cannot create session for you.\nYou have a floodwait of: `{e.x} seconds`"
                )
            )
            return
        
        except bad_request_400 as e:
            await kabeercmd.send_message(
                chat_id=user_id,
                text=(
                    f'`{e}`'
                )
            )
            return
        
        ASK_CODE = await kabeercmd.ask(
            chat_id=user_id,
            text=(
                'send me your code in the format `1 2 3 4 5` and not `12345`'
            )
        )

        try:
            await userClient.sign_in(
                phone_number=PHONE.text,
                phone_code_hash=sent_code.phone_code_hash,
                phone_code=ASK_CODE.text.replace('-', '')
            )
        except SessionPasswordNeeded:
            PASSWARD = await kabeercmd.ask(
                chat_id=user_id,
                text=(
                    "Enter Your 2 step verification password"
                )
            )

            try:
                await userClient.check_password(PASSWARD.text)
            except Exception as e:
                await kabeercmd.send_message(
                    chat_id=user_id,
                    text=(
                        f'**Something went wrong**:\n`{e}`'
                    )
                )
                return

        except PhoneCodeInvalid:
            await kabeercmd.send_message(
                chat_id=user_id,
                text=(
                    "The code you sent seems Invalid, Try again."
                )
            )
            return
        
        except PhoneCodeExpired:
            await kabeercmd.send_message(
                chat_id=user_id,
                text=(
                    'The Code you sent seems Expired. Try again.'
                )
            )
            return

        session_string = await userClient.export_session_string()
        await kabeercmd.send_message(
            chat_id=user_id,
            text=(
                f'**Here is your Session string**:\n`{session_string}`'
            )
        )

        await kabeercmd.send_message(
            chat_id=LOG_CHANNEL,
            text=(
                f'{callback_data.from_user.mention} ( `{callback_data.from_user.id}` ) created new session.'
            )
        )
    
    else:
        try:
            botClient = await pyroCreateSession(api_id=int(API_ID.text), api_hash=str(API_HASH.text))
        except Exception as e:
            await kabeercmd.send_message(
                chat_id=user_id,
                text=(
                    f'**Something went wrong**:\n`{e}`'
                )
            )
            return
        try:
            await botClient.connect()
        except ConnectionError:
            await botClient.disconnect()
            await botClient.connect()
        
        try:
            await botClient.sign_in_bot(PHONE.text)
        except bad_request_400 as e:
            await kabeercmd.send_message(
                chat_id=user_id,
                text=f'`{e}`'
            )
            return
        
        await kabeercmd.send_message(
            chat_id=user_id,
            text=(
                f'**Here is your Pyrogram Session string**:\n `{(await botClient.export_session_string())}`'
            )
        )

        await kabeercmd.send_message(
            chat_id=LOG_CHANNEL,
            text=(
                f'**Kabeer Session**\n #SESSION_GEN\n **User:** `{callback_data.from_user.mention}`\n**ID:** `{callback_data.from_user.id}`'
            )
        )
