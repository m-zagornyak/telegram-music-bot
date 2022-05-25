import asyncio
import json
import locale

import os
import shutil
from urllib.parse import quote

from loader import dp
from data.config import DEEZER_TOKEN

import deezloader.deezloader
import requests

from aiogram import types, exceptions
from aiogram.types import InputMediaAudio
    
from aioify import aioify
from mutagen.mp3 import MP3


locale.setlocale(locale.LC_TIME, '')

DEEZER_URL = "https://deezer.com"
API_URL = "https://api.deezer.com"

API_TRACK = API_URL + "/track/%s"
API_ALBUM = API_URL + "/album/%s"
API_SEARCH_TRK = API_URL + "/search/track/?q=%s"
API_PLAYLIST = API_URL + "/playlist/%s"

DEFAULT_QUALITY = "MP3_320"

try:
    os.mkdir("tmp")
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
        
        
@dp.message_handler(regexp=r"^https?:\/\/(?:www\.)?deezer\.com\/([a-z]*\/)?track\/(\d+)\/?$")
async def get_track(event: types.Message):
    print(event.from_user)
    if event.from_user.id not in downloading_users:
        tmp = event.text
        if tmp[-1] == '/':
            tmp = tmp[:-1]
        tmp_msg = await event.answer(__('downloading'))
        downloading_users.append(event.from_user.id)
        try:
            try:
                dl = await download.download_trackdee(tmp, output_dir="tmp", quality_download=DEFAULT_QUALITY,
                                                      recursive_download=True,
                                                      recursive_quality=True, not_interface=False)
            except:
                # Let's try again...
                await asyncio.sleep(1)
                dl = await download.download_trackdee(tmp, output_dir="tmp", quality_download=DEFAULT_QUALITY,
                                                      recursive_download=True,
                                                      recursive_quality=True, not_interface=False)
            tmp_track = requests.get(API_TRACK % quote(str(event.text.split('/')[-1]))).json()
            tmp_cover = requests.get(tmp_track['album']['cover_xl'], stream=True).raw
            tmp_artist_track = []
            for c in tmp_track['contributors']:
                tmp_artist_track.append(c['name'])
            tmp_date = tmp_track['release_date'].split('-')
            tmp_date = tmp_date[2] + '/' + tmp_date[1] + '/' + tmp_date[0]
            await event.answer_photo(tmp_cover,
                                     caption=('<b>Track: {}</b>'
                                              '\n{} - {}\n<a href="{}">' + __('album_link')
                                              + '</a>\n<a href="{}">' + __('track_link') + '</a>')
                                     .format(
                                         tmp_track['title'], tmp_track['artist']['name'],
                                         tmp_date, tmp_track['album']['link'], tmp_track['link']), parse_mode='HTML'
                                     )

            # Delete user message
            await event.delete()

            tmp_song = open(dl.song_path, 'rb')
            duration = int(MP3(tmp_song).info.length)
            tmp_song.seek(0)
            await event.answer_audio(tmp_song,
                                     title=tmp_track['title'],
                                     performer=', '.join(tmp_artist_track),
                                     duration=duration,
                                     disable_notification=True)
            await tmp_msg.delete()
            tmp_song.close()
            try:
                shutil.rmtree(os.path.dirname(dl.song_path))
            except FileNotFoundError:
                pass
        except Exception as e:
            await tmp_msg.delete()
            await event.answer(__('download_error') + ' ' + str(e))
        finally:
            try:
                downloading_users.remove(event.from_user.id)
            except ValueError:
                pass
    else:
        tmp_err_msg = await event.answer(__('running_download'))
        await event.delete()
        await asyncio.sleep(2)
        await tmp_err_msg.delete()


@dp.message_handler(regexp=r"^https?:\/\/(?:www\.)?deezer\.com\/([a-z]*\/)?album\/(\d+)\/?$")
async def get_album(event: types.Message):
    print(event.from_user)
    if event.from_user.id not in downloading_users:
        tmp = event.text
        if tmp[-1] == '/':
            tmp = tmp[:-1]
        tmp_msg = await event.answer(__('downloading'))
        downloading_users.append(event.from_user.id)
        try:
            try:
                dl = await download.download_albumdee(tmp,
                                                      output_dir="tmp",
                                                      quality_download=DEFAULT_QUALITY,
                                                      recursive_download=True,
                                                      recursive_quality=True,
                                                      not_interface=False)
            except:
                # Let's try again...
                await asyncio.sleep(1)
                dl = await download.download_albumdee(tmp,
                                                      output_dir="tmp",
                                                      quality_download=DEFAULT_QUALITY,
                                                      recursive_download=True,
                                                      recursive_quality=True,
                                                      not_interface=False)
            album = requests.get(API_ALBUM % quote(str(event.text.split('/')[-1]))).json()
            tracks = requests.get(API_ALBUM % quote(str(event.text.split('/')[-1])) + '/tracks?limit=100').json()
            tmp_cover = requests.get(album['cover_xl'], stream=True).raw
            tmp_titles = []
            tmp_artists = []
            for track in tracks['data']:
                tmp_titles.append(track['title'])
                tmp_track = requests.get(API_TRACK % quote(str(track['id']))).json()
                tmp_artist_track = []
                for c in tmp_track['contributors']:
                    tmp_artist_track.append(c['name'])
                tmp_artists.append(tmp_artist_track)
            tmp_date = album['release_date'].split('-')
            tmp_date = tmp_date[2] + '/' + tmp_date[1] + '/' + tmp_date[0]
            await event.answer_photo(tmp_cover,
                                     caption=('<b>Album: {}</b>\n{} - {}\n<a href="{}">' + __('album_link') + '</a>')
                                     .format(
                                         album['title'], album['artist']['name'],
                                         tmp_date, album['link']
                                     ),
                                     parse_mode='HTML')

            # Delete user message
            await event.delete()

            try:
                tmp_count = 0
                group_media = []

                if len(dl.tracks) < 2 or len(dl.tracks) > 10:
                    raise exceptions.NetworkError('One track !')

                all_tracks = []
                for i in dl.tracks:
                    tmp_song = open(i.song_path, 'rb')
                    all_tracks.append(tmp_song)

                for track in all_tracks:
                    duration = int(MP3(track).info.length)
                    track.seek(0)
                    group_media.append(InputMediaAudio(media=track,
                                                       title=tmp_titles[tmp_count],
                                                       performer=', '.join(tmp_artists[tmp_count]),
                                                       duration=duration))
                    tmp_count += 1
                await event.answer_media_group(group_media, disable_notification=True)

                for track in all_tracks:
                    track.close()
            except exceptions.NetworkError:
                tmp_count = 0

                all_tracks = []
                for i in dl.tracks:
                    tmp_song = open(i.song_path, 'rb')
                    all_tracks.append(tmp_song)

                for track in all_tracks:
                    duration = int(MP3(track).info.length)
                    track.seek(0)
                    await event.answer_audio(track,
                                             title=tmp_titles[tmp_count],
                                             performer=', '.join(tmp_artists[tmp_count]),
                                             duration=duration,
                                             disable_notification=True)
                    tmp_count += 1

            await tmp_msg.delete()
            try:
                shutil.rmtree(os.path.dirname(dl.tracks[0].song_path))
            except FileNotFoundError:
                pass

            for track in all_tracks:
                track.close()
        except Exception as e:
            await tmp_msg.delete()
            await event.answer(__('download_error') + ' ' + str(e))
        finally:
            try:
                downloading_users.remove(event.from_user.id)
            except ValueError:
                pass

    else:
        tmp_err_msg = await event.answer(__('running_download'))
        await event.delete()
        await asyncio.sleep(2)
        await tmp_err_msg.delete()


@dp.message_handler(regexp=r"^https?:\/\/(?:www\.)?deezer\.com\/([a-z]*\/)?playlist\/(\d+)\/?$")
async def get_playlist(event: types.Message):
    print(event.from_user)
    if event.from_user.id not in downloading_users:
        tmp = event.text
        if tmp[-1] == '/':
            tmp = tmp[:-1]
        tmp_msg = await event.answer(__('downloading'))
        downloading_users.append(event.from_user.id)
        try:
            try:
                dl = await download.download_playlistdee(tmp,
                                                         output_dir="tmp",
                                                         quality_download=DEFAULT_QUALITY,
                                                         recursive_download=True,
                                                         recursive_quality=True,
                                                         not_interface=False)
            except:
                # Let's try again...
                await asyncio.sleep(1)
                dl = await download.download_playlistdee(tmp,
                                                         output_dir="tmp",
                                                         quality_download=DEFAULT_QUALITY,
                                                         recursive_download=True,
                                                         recursive_quality=True,
                                                         not_interface=False)
            album = requests.get(API_PLAYLIST % quote(str(event.text.split('/')[-1]))).json()
            tracks = requests.get(API_PLAYLIST % quote(str(event.text.split('/')[-1])) + '/tracks?limit=100').json()
            tmp_cover = requests.get(album['picture_xl'], stream=True).raw
            tmp_titles = []
            tmp_artists = []
            for track in tracks['data']:
                tmp_titles.append(track['title'])
                tmp_track = requests.get(API_TRACK % quote(str(track['id']))).json()
                tmp_artist_track = []
                for c in tmp_track['contributors']:
                    tmp_artist_track.append(c['name'])
                tmp_artists.append(tmp_artist_track)
            tmp_count = 0
            tmp_date = album['creation_date'].split(' ')[0].split('-')
            tmp_date = tmp_date[2] + '/' + tmp_date[1] + '/' + tmp_date[0]
            await event.answer_photo(tmp_cover,
                                     caption=('<b>Playlist: {}</b>\n{} - {}\n<a href="{}">'
                                              + __('playlist_link') + '</a>').format(album['title'],
                                                                                     album['creator']['name'],
                                                                                     tmp_date,
                                                                                     album['link']
                                                                                     ),
                                     parse_mode='HTML')

            # Delete user message
            await event.delete()

            all_tracks = []
            for i in dl.tracks:
                tmp_song = open(i.song_path, 'rb')
                all_tracks.append(tmp_song)

            for track in all_tracks:
                duration = int(MP3(track).info.length)
                track.seek(0)
                await event.answer_audio(track,
                                         title=tmp_titles[tmp_count],
                                         performer=', '.join(tmp_artists[tmp_count]),
                                         duration=duration,
                                         disable_notification=True)
                tmp_count += 1
            await tmp_msg.delete()

            for i in dl.tracks:
                try:
                    shutil.rmtree(os.path.dirname(i.song_path))
                except FileNotFoundError:
                    pass

            for i in all_tracks:
                i.close()
        except Exception as e:
            await tmp_msg.delete()
            await event.answer(__('download_error') + ' ' + str(e))
        finally:
            try:
                downloading_users.remove(event.from_user.id)
            except ValueError:
                pass
    else:
        tmp_err_msg = await event.answer(__('running_download'))
        await event.delete()
        await asyncio.sleep(2)
        await tmp_err_msg.delete()



