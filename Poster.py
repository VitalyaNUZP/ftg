"""
    ____  __  __ _                            __ _   _  _   _           _     _
   / __ \|  \/  (_)_ __   ___  ___ _ __ __ _ / _| |_| || | | |__   __ _| |__ (_) ___  ___
  / / _` | |\/| | | '_ \ / _ \/ __| '__/ _` | |_| __| || |_| '_ \ / _` | '_ \| |/ _ \/ __|
 | | (_| | |  | | | | | |  __/ (__| | | (_| |  _| |_|__   _| |_) | (_| | |_) | |  __/\__ \
  \ \__,_|_|  |_|_|_| |_|\___|\___|_|  \__,_|_|  \__|  |_| |_.__/ \__,_|_.__/|_|\___||___/
   \____/
"""
#добавить возможность пересылвать сообщения не только из @air_alert_ua, а из любого канала
from .. import loader, utils

def register(cb):
    cb(PosterMod())

@loader.tds
class PosterMod(loader.Module):
    """Делает посты для канала. Настройка ІD канала в .config(GEEK-TG)"""
    strings = {'cfg_doc': 'Настройка надписей состояния работы',
               "name": "Poster",
               'Working': '<code>[Poster]</code><b>Оформление...</b>',
               'NoReplyOrMedia': '<code>[Poster]</code><b>Нужен реплай на медиа.</b>',
               'Error': '<code>[Poster]</code><b>Произошла ошибка.(проверьте конфиг и сам канал)</b>',
               'NoConfig': '<code>[Poster]</code><b>Не настроен конфиг модуля.</b>'}

    def __init__(self):
        self.name = self.strings['name']

    def __init__(self):
        self.config = loader.ModuleConfig(
            'Channel', 'Нужен ID канала', lambda: 'Канал, в которий идёт постинг.',
            'Chat', 'Нужен ID чата', lambda: 'Чат, в который идёт постинг.')

    @loader.unrestricted
    async def postcmd(self, message):
        """<Подпись к посту(необяз.)>


        👨‍💻Made by: @Minecraft4babies_GFTG_Modules"""

        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)
        messages_to_post = []
        caption = []
        files = []

        if reply:
            if reply.media:
                await message.edit(self.strings['Working'])
                try:
                    if reply.grouped_id:
                        for i in range(0,10):
                            checked_message = await message.client.get_messages(message.chat_id, ids=reply.id - i)
                            try:
                                if reply.grouped_id == checked_message.grouped_id:
                                    messages_to_post.insert(0, checked_message)
                            except AttributeError:
                                None
                        for i in range(1,10):
                            checked_message = await message.client.get_messages(message.chat_id, ids=reply.id + i)
                            try:
                                if reply.grouped_id == checked_message.grouped_id:
                                    messages_to_post.append(checked_message)
                            except AttributeError:
                                None
                    else:
                        messages_to_post.append(reply)

                    for i in messages_to_post:
                        files.append(i.media)

                    for i in range(1, len(files)):
                        caption.append('')

                    caption.append(args)

                    await message.client.send_file(int(self.config['Channel']), files, caption=caption)  # Отправка

                    for i in messages_to_post:
                        await i.delete()
                        await message.delete()
                except:
                    if self.config['Channel'] == 'Нужен ID канала':
                        await message.edit(self.strings['NoConfig'])
                    else:
                        await message.edit(self.strings['Error'])
            else:
                await message.edit(self.strings['NoReplyOrMedia'])
        else:
            await message.edit(self.strings['NoReplyOrMedia'])
#
    async def post1cmd(self, message):
        """<ID канала> <ID чата>


        👨‍💻Made by: @Minecraft4babies_GFTG_Modules"""
        args = utils.get_args_raw(message)
        args = args.split()
        reply = await message.get_reply_message()
        if len(args) == 2:
            await message.edit('<code>[Poster]</code><b>Оформление...</b>')
            pgf = message.client.get_messages(int(args[0]), limit=1)
            try:
                await message.client.send_message(int(args[1]), file=pgf.media, reply_to=reply)
                await message.delete()
            except:
                await message.edit('<code>[Poster]</code><b>Произошла ошибка.</b>')
        else:
            await message.edit('<code>[Poster]</code><b>Неверное количество аргументов.</b>')
