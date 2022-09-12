#   Coded edit vitalyatroz #
#     t.me/vitalyatroz     #


# Слава Україні! Героям слава!

from .. import loader, utils

from telethon.errors.rpcerrorlist import MessageNotModifiedError

import logging
import asyncio

logger = logging.getLogger(__name__)


@loader.tds
class adsMod(loader.Module):
    """Автор by @vitalyatroz"""
    
    strings = {"name": "Текстова анімація",
               "no_message": "<b>Повідомлення не знайдено</b>",
               "type_char_cfg_doc": "Затримка між символами",
               "delay_typer_cfg_doc": "Затримка між символами",
               "delay_text_cfg_doc": "Затримка між повідомленнями",}

    def __init__(self):
        self.config = loader.ModuleConfig("DELAY_TYPER", 0.10, lambda m: self.strings("delay_typer_cfg_doc", m),
                                          "DELAY_TEXT", 0.5, lambda m: self.strings("delay_text_cfg_doc", m))

    @loader.ratelimit
    async def adscmd(self, message):
        """Робить текстову анімацію з вказаного повідомлення .ads <Текст>"""
        args = utils.get_args(message)
        if not args:
            await utils.answer(message, self.strings("no_message", message))
            return
        if len(args) == 1:
            await utils.answer(message, self.strings("no_message", message))
            return
        try:
            count = int(args[0])
        except ValueError:
            await utils.answer(message, "<b>Повідомлення не знайдено</b>")
            return
        
        a = " ".join(args[1:])
        reply = await message.get_reply_message()

        if reply:
            a = reply.raw_text
        for _ in range(count):

            for c in a:
                a = a[-1]+a[0:-1]
                message = await utils.answer(message, "⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠"+a+"⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠⁠")
                await asyncio.sleep(0.1)
