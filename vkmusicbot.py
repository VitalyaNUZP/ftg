#бот в телеграм который скачивает музыку с вк
#Использовать библиотеку vk_api для скачивания музыки с вк и отправки ее в телеграм бота
#добавить возможность управления кнопками следующая/предыдущая песня
#Токен бота: 2050884335:AAHkgzYQnFALA9F6cQ4BM1XPCcVy3-relaY


# import asyncio
# import logging
# import os
# import re
# import sys
# import time
# import traceback
# from io import BytesIO
# from pathlib import Path
# from typing import Union
# 
# import httpx
# from telethon import TelegramClient, events
# from telethon.errors import MessageNotModifiedError
# from telethon.events import StopPropagation
# from telethon.tl.custom import Button
# from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
# from telethon.tl.types import (
#     DocumentAttributeAudio,
#     DocumentAttributeFilename,
#     InputBotInlineMessageID,
#     InputMediaDocument,
#     InputMediaPhoto,
#     InlineBotSwitchPM,
#     InlineKeyboardButtonUrl,
# )
# 
# from .. import loader, utils
# 
# logger = logging.getLogger(__name__)
# 
# 
# @loader.tds
# class VkMusicMod(loader.Module):
#     """VkMusic"""
#     strings = {
#         "name": "VkMusic",
#         "no_args": "<b>Нету аргументов.</b>",
#         "no_music": "<b>Музыка с названием <code>{}</code> не найдена.</b>",
#         "no_reply": "<b>Нету реплая.</b>",
#         "no_track": "<b>Нету трека.</b>",
#         "no_yt": "<b>Нету видео с названием <code>{}</code>.</b>",
#         "no_yt_args": "<b>Нету аргументов.</b>",
#         "search": "Найдено",
#         "searching": "<b>Поиск...</b>",
#         "uploading": "<b>Загрузка...</b>",
#         "yt": "YouTube",
#     }
# 
#     def __init__(self):
#         self.config = loader.ModuleConfig("API_ID", 0, lambda m: self.strings("no_api_id", m))
#         self.name = self.strings["name"]
# 
#     async def client_ready(self, client, db):
#         self.client = client
#         self.db = db
# 
#     async def inline_handler(self, inline

import asyncio
import logging
import os
import re
import sys
import time
import traceback
from io import BytesIO
from pathlib import Path
from typing import Union

import httpx
from telethon import TelegramClient, events
from telethon.errors import MessageNotModifiedError
from telethon.events import StopPropagation
from telethon.tl.custom import Button
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
from telethon.tl.types import (
    DocumentAttributeAudio,
    DocumentAttributeFilename,
    InputBotInlineMessageID,
    InputMediaDocument,
    InputMediaPhoto,
    InlineBotSwitchPM,
    InlineKeyboardButtonUrl,
)

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class VkMusicMod(loader.Module):
    """VkMusic"""
    strings = {
        "name": "VkMusic",
        "no_args": "<b>Нету аргументов.</b>",
        "no_music": "<b>Музыка с названием <code>{}</code> не найдена.</b>",
        "no_reply": "<b>Нету реплая.</b>",
        "no_track": "<b>Нету трека.</b>",
        "no_yt": "<b>Нету видео с названием <code>{}</code>.</b>",
        "no_yt_args": "<b>Нету аргументов.</b>",
        "search": "Найдено",
        "searching": "<b>Поиск...</b>",
        "uploading": "<b>Загрузка...</b>",
        "yt": "YouTube",
    }

    def __init__(self):
        self.config = loader.ModuleConfig("API_ID", "2050884335:AAHkgzYQnFALA9F6cQ4BM1XPCcVy3-relaY", lambda m: self.strings("no_api_id", m))
        self.name = self.strings["name"]

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    async def inline_handler(self, inline):
        if inline.query.user_id == self.client.uid:
            return
        if not inline.query.query:
            return
        if not inline.query.query.startswith("vk"):
            return
        if not inline.query.query[2:]:
            return
        query = inline.query.query[2:]
        await inline.answer(
            [
                await self._get_music(query),
            ],
            switch_pm=InlineBotSwitchPM(
                self.strings("search", inline.query.peer_id),
                "vk",
            ),
        )

    async def vkcmd(self, message):
        """Использование: .vk <название>."""
        args = utils.get_args_raw(message)
        if not args:
            return await message.edit(self.strings("no_args", message))
        await message.edit(self.strings("searching", message))
        music = await self._get_music(args)
        if not music:
            return await message.edit(self.strings("no_music", message).format(args))
        await message.delete()
        await self.client.send_file(message.to_id, music, reply_to=message.reply_to_msg_id)

    async def _get_music(self, query):
        async with httpx.AsyncClient() as client:
            r = await client.get(
                "https://api.vk.com/method/audio.search",
                params={
                    "access_token": "f0a8c5e5f0a8c5e5f0a8c5e5b2f0d9c0aaff0a8f0a8c5e5d3f3c1c2b1a9b9e9b6e9d8",
                    "v": "5.103",
                    "q": query,
                    "count": 1,
                },
            )
        try:
            music = r.json()["response"]["items"][0]
        except IndexError:
            return
        url = music["url"]
        title = music["title"]
        artist = music["artist"]
        duration = music["duration"]
        async with httpx.AsyncClient() as client:
            r = await client.get(url)
        file = BytesIO(r.content)
        file.name = f"{artist} - {title}.mp3"
        file.seek(0)
        return InputMediaDocument(
            file,
            attributes=[
                DocumentAttributeAudio(duration, title=title, performer=artist),
                DocumentAttributeFilename(file.name),
            ],
        )
        