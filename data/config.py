import os

from dotenv import load_dotenv

load_dotenv()
""" 
BOT_TOKEN = '5347241093:AAHhBE-pyCpUDQitwmbZG0BNnLsnbJg5u2E'
CHANNEL_ID = ''
DEEZER_TOKEN = '7ef30c302ba40f8021d74b31b954ee188c08ec3644620472fe6494490abd2b205fb3bf5545942e7b460502eed93b5ce9d60b91c8298a0c3a7ea2a402419568556acf1a826f4512e69820d7285c180642067905c2b0bcc005944ef7eee359d545 '
PATH = ''
"""


BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
DEEZER_TOKEN = str(os.getenv("DEEZER_TOKEN"))
CHANNEL_ID = str(os.getenv("CHANNEL_ID"))
API_URL = str(os.getenv("API_URL"))

DEEZER_URL = 'https://deezer.com'

DEFAULT_QUALITY = "MP3_320"


