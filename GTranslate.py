from .. import loader, utils
from googletrans import LANGUAGES, Translator


@loader.tds
class TranslatorMod(loader.Module):
    """Гугл Перекладач"""
    strings = {'name': 'GTranslate'}

    async def trslcmd(self, message):
        """Використовуй: .trsl <з якого мови перекласти> <на який перекласти> <текст> або .trsl <на який перекласти> <реплай>; langs."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        langs = LANGUAGES
        lang = args.split()
        tr = Translator().translate
        if not args and not reply:
            return await message.edit("Немає аргументів чи реплаю")
        if args == "langs":
            return await message.edit("<code>" + '\n'.join(str(langs).split(', ')) + "</code>")
        if reply:
            try:
                trslreply = True
                text = reply.text
                if len(lang) >= 2:# якщо не вказано мову, то використовується англійська
                    trslreply = False
                dest = 'uk' # Українська мова за замовчуванням при реплаї якщо не вказано іншу мову
                r = tr(args.split(' ', 1)[1] if trslreply is False else text, dest=dest)
            except: r = tr(reply.text)
        else:
            try:
                try:
                    src = langs[lang[0]]
                    dest = langs[lang[1]]
                    text = args.split(' ', 2)[2]
                    r = tr(text, src=src, dest=dest)
                except:
                    #мова перекладу по замовчуванню це українська
                    dest = 'uk'
                    text = args.split(' ', 1)[1]
                    r = tr(text, dest=dest)
            except KeyError: r = tr(args)
        return await message.edit(f"<b>[{r.src} ➜ {r.dest}]</b>\n{r.text}")