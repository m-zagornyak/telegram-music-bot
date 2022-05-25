import asyncio
import io
import json
import locale

import os
import shutil
import traceback

from loader import dp, bot
from data.config import DEEZER_TOKEN

import deezloader.deezloader
import requests
from PIL import Image
from aiogram import types

from aioify import aioify
from mutagen.id3 import ID3, APIC, error
from mutagen.mp3 import MP3
from yt_dlp import YoutubeDL

locale.setlocale(locale.LC_TIME, '')


try:
    os.mkdir("tmp")
except FileExistsError:
    pass

try:
    os.mkdir("tmp/yt/")
except FileExistsError:
    pass


deezloader_async = aioify(obj=deezloader.deezloader, name='deezloader_async')

download = deezloader_async.DeeLogin(DEEZER_TOKEN)
downloading_users = []



LANGS_FILE = json.load( open(r'E:\\python\\Music-telegram-bot\\utils\\langs.json') )
LANG = os.environ.get('BOT_LANG')

if LANG is not None:
    print("Lang : " + LANG)
else:
    print("Lang : en")
    LANG = 'en'


def __(s):
    return LANGS_FILE[s][LANG]


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


@dp.message_handler(regexp=r"^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+")
async def get_youtube_audio(event: types.Message):
    print(event.from_user)
    if event.from_user.id not in downloading_users:
        tmp_msg = await event.answer(__('downloading'))
        downloading_users.append(event.from_user.id)
        try:
            ydl_opts = {
                'outtmpl': 'tmp/yt/%(id)s.%(ext)s',
                'format': 'bestaudio/best',
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320'}],
            }

            # Download file
            ydl = YoutubeDL(ydl_opts)
            dict_info = ydl.extract_info(event.text, download=True)

            thumb = dict_info["thumbnail"]

            # Get thumb
            content = requests.get(thumb).content
            image_bytes = io.BytesIO(content)

            upload_date = "Unknown date"
            try:
                if dict_info is not None and dict_info["upload_date"] is not None:
                    upload_date = dict_info["upload_date"]
                    upload_date = upload_date[6:8] + "/" + upload_date[4:6] + "/" + upload_date[0:4]
            except:
                pass

            # Send cover
            await event.answer_photo(image_bytes.read(),
                                     caption=('<b>Track: {}</b>'
                                              '\n{} - {}\n\n<a href="{}">' + __('track_link') + '</a>')
                                     .format(
                                         dict_info['title'],
                                         dict_info["uploader"], upload_date,
                                         "https://youtu.be/" + dict_info["id"]
                                     ),
                                     parse_mode='HTML'
                                     )

            # Delete user message
            await event.delete()

            location = "tmp/yt/" + dict_info["id"] + '.mp3'
            tmp_song = open(location, 'rb')

            # TAG audio
            audio = MP3(location, ID3=ID3)
            try:
                audio.add_tags()
            except error:
                pass
            audio.tags.add(APIC(mime='image/jpeg', type=3, desc=u'Cover', data=image_bytes.read()))
            audio.save()

            # Create thumb
            roi_img = crop_center(Image.open(image_bytes), 80, 80)
            img_byte_arr = io.BytesIO()
            roi_img.save(img_byte_arr, format='jpeg')

            # Send audio
            await event.answer_audio(tmp_song,
                                     title=dict_info['title'],
                                     performer=dict_info['uploader'],
                                     thumb=img_byte_arr.getvalue(),
                                     disable_notification=True)
            tmp_song.close()
            try:
                shutil.rmtree(os.path.dirname(location))
            except FileNotFoundError:
                pass
        except Exception as e:
            traceback.print_exc()
            await event.answer(__('download_error') + ' ' + str(e))
        finally:
            await tmp_msg.delete()
            try:
                downloading_users.remove(event.from_user.id)
            except ValueError:
                pass
    else:
        tmp_err_msg = await event.answer(__('running_download'))
        await event.delete()
        await asyncio.sleep(2)
        await tmp_err_msg.delete()


