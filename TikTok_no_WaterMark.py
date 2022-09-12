#   Coded edit vitalyatroz #
#     t.me/vitalyatroz     #

# Слава Україні! Героям слава!
from .. import loader, utils


def register(cb):
    cb(TikTokMod())

class TikTokMod(loader.Module):
    """Модуль для завантаження відео з TikTok"""
    strings = {'name': 'TikTok no WaterMark'}

    async def tikcmd(self, message):
        """Використовуйте: .tik <посилання на відео>."""
        await utils.answer(message, 'Завантаження відео...')
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "Введіть посилання на відео.")
            return
        r = await message.client.inline_query('tikdobot', args)
        await message.client.send_file(message.to_id, r[1].result.content.url)
        await message.delete()