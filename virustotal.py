from .. import loader, utils, main
import asyncio

@loader.tds
class VirusTotal(loader.Module):
  strings = {"name": "VirusTotal"}
  """VirusTotal by @vitalyatroz"""
  async def vtcmd(self, message):
    """ Отправляет файл на проверку
    .vt <reply>"""
    reply = await message.get_reply_message()
    await message.edit("<b>Зачекай...</b>")
    try:
      await message.client.send_file(1356559037, reply.media)
      await asyncio.sleep(5)
      messages = await message.client.get_messages('Telegram')
      messages[0].click()
      await asyncio.sleep(2)
      for i in range(3):
        messages2 = await message.client.get_messages(1356559037)
        await message.edit(str(messages2[0].message))
        await asyncio.sleep(20)
    except Exception as ex:
      await message.edit(str(ex))