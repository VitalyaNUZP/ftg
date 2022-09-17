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
# Работает через бота @vkmusic_bot, а також @lybot и @vkmusbot
# Author: SekaiYoneya
# Edit: @vitalyatroz
# Commands:
# .sm / .sm2 / .sm3 - поиск музыки по разным ботам
# ---------------------------------------------------------------------------------

# @Sekai_Yoneya / @vitalyatroz


import logging
import xml.etree.ElementTree as ET
from typing import Union

import httpx
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           InlineQueryResultArticle, InputTextMessageContent)
from bs4 import BeautifulSoup

from .. import loader, utils
from ..inline.types import InlineQuery
from ..utils import rand


@loader.tds
class SearchMusicMod(loader.Module):
    """
    Модуль SearchMusic - поиск музыки
    Работает через бота @vkmusic_bot, @lybot и @vkmusbot
    """

    strings = {"name": "SearchMusic"}

    async def smcmd(self, message):
        """ - «название» чтобы найти музыку в @vkmusic_bot."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not args:
            return await message.edit("<b>Нету аргументов.</b>")
        try:
            await message.edit("<b>Загрузка...</b>")
            music = await message.client.inline_query("vkmusic_bot", args)
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
    
    async def sm2cmd(self, message):
        """ - «название» чтобы найти музыку в @lybot."""
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
    
    async def sm3cmd(self, message):
        """ - «название» чтобы найти музыку в @vkmusbot."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not args:
            return await message.edit("<b>Нету аргументов.</b>")
        try:
            await message.edit("<b>Загрузка...</b>")
            music = await message.client.inline_query("vkmusbot", args)
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
    async def smallcmd(self, message):
        """ - «название» чтобы найти музыку."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not args:
            return await message.edit("<b>Нету аргументов.</b>")
        try:
            await message.edit("<b>Загрузка...</b>")
            music = await message.client.inline_query("vkmusic_bot", args)
            music2 = await message.client.inline_query("lybot", args)
            music3 = await message.client.inline_query("vkmusbot", args)
            await message.delete()
            await message.client.send_file(
                message.to_id,
                music[0].result.document,
                reply_to=reply.id if reply else None,
            )
            await message.client.send_file(
                message.to_id,
                music2[0].result.document,
                reply_to=reply.id if reply else None,
            )
            await message.client.send_file(
                message.to_id,
                music3[0].result.document,
                reply_to=reply.id if reply else None,
            )
        except:
            return await message.client.send_message(
                message.chat_id,
                f"<b>Музыка с названием <code>{args}</code> не найдена.</b>",
            )