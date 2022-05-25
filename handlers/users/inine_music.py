from aiogram import types, exceptions
from aiogram.types import (
    InlineQuery,
    InputTextMessageContent, 
    InlineQueryResultArticle, 
    )

import re
import requests
from urllib.parse import quote

from loader import dp


DEEZER_URL = "https://deezer.com"
API_URL = "https://api.deezer.com"

API_TRACK = API_URL + "/track/%s"
API_ALBUM = API_URL + "/album/%s"
API_SEARCH_TRK = API_URL + "/search/track/?q=%s"
API_PLAYLIST = API_URL + "/playlist/%s"

DEFAULT_QUALITY = "MP3_320"


@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    items = []
    if inline_query.query:
        album = False
        if inline_query.query.startswith('artist '):
            album = True
            tmp_text = 'artist:"{}"'.format(inline_query.query.split('artist ')[1])
            text = API_SEARCH_TRK % quote(str(tmp_text))
        elif inline_query.query.startswith('track '):
            tmp_text = 'track:"{}"'.format(inline_query.query.split('track ')[1])
            text = API_SEARCH_TRK % quote(str(tmp_text))
        elif inline_query.query.startswith('album '):
            album = True
            tmp_text = 'album:"{}"'.format(inline_query.query.split('album ')[1])
            text = API_SEARCH_TRK % quote(str(tmp_text))
        else:
            text = API_SEARCH_TRK % quote(str(inline_query.query))

        try:
            r = requests.get(text).json()
            all_ids = []
            for i in r['data']:
                tmp_url = i['album']['tracklist']
                tmp_id = re.search('/album/(.*)/tracks', tmp_url).group(1)
                if not (album and tmp_id in all_ids):
                    tmp_album = requests.get(API_ALBUM % quote(str(tmp_id))).json()
                    all_ids.append(tmp_id)
                    tmp_date = tmp_album['release_date'].split('-')
                    tmp_date = tmp_date[2] + '/' + tmp_date[1] + '/' + tmp_date[0]
                    if album:
                        title = i['album']['title']
                        tmp_input = InputTextMessageContent(DEEZER_URL + "/album/%s" % quote(str(tmp_id)))
                        try:
                            nb = str(len(tmp_album['tracks']['data'])) + ' audio(s)'
                        except KeyError:
                            nb = ''
                        show_txt_album = ' | ' + nb + ' (album)'
                    else:
                        show_txt_album = ''
                        tmp_input = InputTextMessageContent(i['link'])
                        title = i['title']

                    result_id: str = i['id']
                    items.append(InlineQueryResultArticle(
                        id=result_id,
                        title=title,
                        description=i['artist']['name'] + ' | ' + tmp_date + show_txt_album,
                        thumb_url=i['album']['cover_small'],
                        input_message_content=tmp_input,
                    ))
        except KeyError as e:
            print(e)
            pass
        except AttributeError as e:
            print(e)
            pass
    await dp.answer_inline_query(inline_query.id, results=items, cache_time=300)