#   Coded edit vitalyatroz #
#     t.me/vitalyatroz     #

# Слава Україні! Героям слава!

from .. import loader, utils 
from telethon import events 
from telethon.errors.rpcerrorlist import YouBlockedUserError 
from asyncio.exceptions import TimeoutError 
 
 
def register(cb): 
    cb(WikiMod()) 
 
class WikiMod(loader.Module): 
    """Модуль для пошуку по вікіпедії""" 
    strings = {'name': 'tanya_ua'} 
 
    async def wikicmd(self, message): 
        """Пиши .tanya + слово для пошуку""" 
        try: 
            text = utils.get_args_raw(message) 
            reply = await message.get_reply_message() 
            chat = "@just_zhenya_bot" 
            if not text and not reply: 
                await message.edit("<b>Введіть слово або відповідь на повідомлення</b>") 
                return 
            if text: 
                await message.edit("<b>Шукаю...</b ") 
                async with message.client.conversation(chat) as conv: 
                    try: 
                        response = conv.wait_event(events.NewMessage(incoming=True, from_users=528677877)) 
                        await message.client.send_message(chat, "/tanya " + text) 
                        response = await response 
                    except YouBlockedUserError: 
                        await message.reply("<b>Розблокуй: @just_zhenya_bot</b>")
                        return 
                    if not response.text: 
                        await message.edit("<Помилка</b>")
                        return 
                    await message.delete() 
                    await message.client.send_file(message.to_id, media) 
            if reply: #переслать последнюю звуковую запись
                await message.edit("<b>Шукаю...</b>")
                async with message.client.conversation(chat) as conv:
                    try:
                        response = conv.wait_event(events.NewMessage(incoming=True, from_users=528677877))
                        await message.client.send_message(chat, "/tanya " + reply.text)
                        response = await response
                    except YouBlockedUserError:
                        await message.reply("<b>Розблокуй: @just_zhenya_bot</b>")
                        return
                    if not response.text:
                        await message.edit("<Помилка</b>")
                        return
                    await message.delete()
                    await message.client.send_file(message.to_id, media) 
        except TimeoutError: 
            return await message.edit("<b>Помилка</b>")
