#   Coded edit vitalyatroz #
#     t.me/vitalyatroz     #

# Слава Україні! Героям слава!


import os

from telethon.tl.types import DocumentAttributeAudio
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    DownloadError,
    ContentTooShortError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)

from .. import loader, utils


@loader.tds
class YtDlMod(loader.Module):
    """Youtube-Dl Модуль"""

    strings = {
        "name": "Youtube-Dl",
        "preparing": "<b>[YouTube-Dl]</b> Підготовка...",
        "downloading": "<b>[YouTube-Dl]</b> Завантаження...",
        "working": "<b>[YouTube-Dl]</b> Обробка...",
        "exporting": "<b>[YouTube-Dl]</b> Експорт...",
        "reply": "<b>[YouTube-Dl]</b> Лінк не знайдено!",
        "noargs": "<b>[YouTube-Dl]</b> Не знайдено аргументів!",
        "content_too_short": "<b>[YouTube-Dl]</b> Завантаження відео не вдалося!",
        "geoban": "<b>[YouTube-Dl]</b> Відео заборонено в вашій країні!",
        "maxdlserr": '<b>[YouTube-Dl]</b> Достигнуто максимальна кількість завантажень!',
        "pperr": "<b>[YouTube-Dl]</b> Помилка після завантаження!",
        "noformat": "<b>[YouTube-Dl]</b> Не знайдено формат!",
        "xameerr": "<b>[YouTube-Dl]</b> {0.code}: {0.msg}\n{0.reason}",
        "exporterr": "<b>[YouTube-Dl]</b> Помилка експорту!",
        "err": "<b>[YouTube-Dl]</b> {}",
        "err2": "<b>[YouTube-Dl]</b> {}: {}",
    }

    async def yvcmd(self, m):
        """.yv <link / reply_to_link> - Завантажити відео"""
        await riper(self, m, "video")

    async def yacmd(self, m):
        """.ya <link / reply_to_link> - Завантажити аудіо"""
        await riper(self, m, "audio")


async def riper(self, m, type):
    reply = await m.get_reply_message()
    args = utils.get_args_raw(m)
    url = args or reply.raw_text
    if not url:
        return await utils.answer(m, self.strings("noargs", m))
    m = await utils.answer(m, self.strings("preparing", m))
    if type == "audio":
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
        video = False
        song = True
    elif type == "video":
        opts = {
            "format": "best",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            ],
            "outtmpl": "%(id)s.mp4",
            "logtostderr": False,
            "quiet": True,
        }
        song = False
        video = True
    try:
        await utils.answer(m, self.strings("downloading", m))
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        return await utils.answer(m, self.strings("err", m).format(str(DE)))
    except ContentTooShortError:
        return await utils.answer(m, self.strings("content_too_short", m))
    except GeoRestrictedError:
        return await utils.answer(m, self.strings("geoban", m))
    except MaxDownloadsReached:
        return await utils.answer(m, self.strings("maxdlserr", m))
    except PostProcessingError:
        return await utils.answer(m, self.strings("pperr", m))
    except UnavailableVideoError:
        return await utils.answer(m, self.strings("noformat", m))
    except XAttrMetadataError as XAME:
        return await utils.answer(m, self.strings("xameerr", m).format(XAME))
    except ExtractorError:
        return await utils.answer(m, self.strings("exporterr", m))
    except Exception as e:
        return await utils.answer(
            m, self.strings("err2", m).format(str(type(e)), str(e))
        )
    if song:
        u = rip_data["uploader"] if "uploader" in rip_data else "Northing"
        await utils.answer(
            m,
            open(f"{rip_data['id']}.mp3", "rb"),
            supports_streaming=True,
            reply_to=reply.id if reply else None,
            attributes=[
                DocumentAttributeAudio(
                    duration=int(rip_data["duration"]),
                    title=str(rip_data["title"]),
                    performer=u,
                )
            ],
        )
        os.remove(f"{rip_data['id']}.mp3")
    elif video:
        await utils.answer(
            m,
            open(f"{rip_data['id']}.mp4", "rb"),
            reply_to=reply.id if reply else None,
            supports_streaming=True,
            caption=rip_data["title"],
        )
        os.remove(f"{rip_data['id']}.mp4")
