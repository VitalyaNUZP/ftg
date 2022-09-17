# ---------------------------------------------------------------------------------
#  ,_     _          
#  |\_,-~/          
#  / _  _ |    ,--.  🌐 This module was loaded through https://t.me/hikkamods_bot
# (  @  @ )   / ,-'  🔓 Not licensed.
#  \  _T_/-._( (     
#  /         `. \    ⚠️ Owner of this bot doesn't take responsibility for any
# |         _  \ |   errors caused by this module or this module being non-working
#  \ \ ,  /      |   and doesn't take ownership of any copyrighted material.
#   || |-_\__   /    
#  ((_/`(____,-'     
# ---------------------------------------------------------------------------------
# Name: SearchMusic
# Description: Модуль SearchMusic - поиск музыки
# Работает через бота @lybot а також @vkmusic_bot
# Author: SekaiYoneya
# Commands:
# .sm / .s
# ---------------------------------------------------------------------------------

# @Sekai_Yoneya / @vitalyatroz

from .. import loader, utils


@loader.tds
class SearchMusicMod(loader.Module):
    """
    Модуль SearchMusic - поиск музыки
    Работает через бота @lybot а також @vkmusic_bot
    """

    strings = {"name": "SM by @vitalyatroz"}

    async def smcmd(self, message):
        """Используй: .sm «название» чтобы найти музыку по названию."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not args:
            return await message.edit("<b>Нету аргументов.</b>")
        try:
            await message.edit("<b>Загрузка...</b>")
            music = await message.client.inline_query("lybot", args)
            await message.delete()
            await message.client.send_file(
                message.to_id,
                music[0].result.document,
                reply_to=reply.id if reply else None,
            )
        except:
            return await message.client.send_message(
                message.chat_id,
                f"<b>Музыка с названием <code>{args}</code> не найдена.</b>",
            )
     async def scmd(self, message):
        """Використовуй: .s «назва» щоб знайти музику по назві."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not args:
            return await message.edit("<b>Немає аргументів.</b>")
        try:
            await message.edit("<b>Завантаження...</b>")
            music = await message.client.inline_query("vkmusic_bot", args)
            await message.delete()
            await message.client.send_file(
                message.to_id,
                music[0].result.document,
                reply_to=reply.id if reply else None,
            )
        except:
            return await message.client.send_message
                message.chat_id,
                f"<b>Музика з назвою <code>{args}</code> не знайдена.</b>",
            )
            