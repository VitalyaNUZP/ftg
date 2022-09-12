#   Coded edit vitalyatroz #
#     t.me/vitalyatroz     #

# Слава Україні! Героям слава!
from .. import loader, utils
import json
import io
import requests
from PIL import Image
import random
import string

@loader.tds
class YandexReverseSearchMod(loader.Module):
    """Реверсивний пошук зображень через Яндекс (він найкращий, як на мене)"""
    strings = {"name": "Яндекс Реверс",
               "search": "⚪⚪⚪\n⚪❓⚪\n⚪⚪⚪",
               "no_reply": "<b>Немає відповіді на зображення/стікер.</b>",
               "result": '<a href="{}"><b>🔴⚪🔴|Дивлюсь</b>\n<b>⚪🔴⚪|Шукаю</b>\n<b>⚪🔴⚪|Результат</b></a>',
               "error": '<b>Щось пішло не так...</b>'}
               
    @loader.owner
    async def yarscmd(self, message):
        """.yars <repy to image>"""
        reply = await message.get_reply_message()
        data = await check_media(message, reply)
        if not data:
            await utils.answer(message, self.strings("no_reply", message))
            return
        await utils.answer(message, self.strings("search", message))
        searchUrl = 'https://yandex.ru/images/search'
        files = {'upfile': ('blob', data, 'image/jpeg')}
        params = {'rpt': 'imageview', 'format': 'json', 'request': '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'}
        response = requests.post(searchUrl, params=params, files=files)
        if response.ok:
            query_string = json.loads(response.content)['blocks'][0]['params']['url']
            link = searchUrl + '?' + query_string
            text = self.strings("result", message).format(link)
            await utils.answer(message, text)
        else:
        	await utils.answer(message, self.strings("error", message))
        
async def check_media(message, reply):
    if reply and reply.media:
        if reply.photo:
            data = reply.photo
        elif reply.document:
            if reply.gif or reply.video or reply.audio or reply.voice:
                return None
            data = reply.media.document
        else:
            return None
    else:
        return None
    if not data or data is None:
        return None
    else:
        data = await message.client.download_file(data, bytes)
        img = io.BytesIO(data)
        return img
