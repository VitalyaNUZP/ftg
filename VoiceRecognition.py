#   Coded edit vitalyatroz #
#     t.me/vitalyatroz     #
#      meta developer:     #
#        @D4n13l3k00       #

# requires: pydub speechRecognition | pip install pydub speechRecognition
# Слава Україні! Героям слава!

from io import BytesIO

import speech_recognition as srec
from pydub import AudioSegment as auds

from .. import loader, utils


@loader.tds
class VoiceRecognitionMod(loader.Module):
    "Розпізнавання голосу за допомогою Google Speech Recognition API"
    strings = {"name": "Розпізнавання голосу", "pref": "<b>[VRC]</b> "}

    @loader.owner
    async def recvcmd(self, m):
        ".recv <reply to voice/audio> - розпізнати голос"
        reply = await m.get_reply_message()
        if reply and reply.file.mime_type.split("/")[0] == "аудіо":
            m = await utils.answer(m, self.strings["pref"] + "Завантаження...")
            source = BytesIO(await reply.download_media(bytes))
            source.name = reply.file.name
            out = BytesIO()
            out.name = "recog.wav"
            m = await utils.answer(m, self.strings["pref"] + "Конвертація...")
            auds.from_file(source).export(out, "wav")
            out.seek(0)
            m = await utils.answer(m, self.strings["pref"] + "Розпізнавання...")
            recog = srec.Recognizer()
            sample_audio = srec.AudioFile(out)
            with sample_audio as audio_file:
                audio_content = recog.record(audio_file)
            await utils.answer(
                m,
                self.strings["pref"]
                + recog.recognize_google(audio_content, language="ru-RU"),
            )
        else:
            await utils.answer(m, self.strings["pref"] + "Відповіть на audio/voice...")
