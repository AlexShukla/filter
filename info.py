import re
import os
from os import environ
from pyrogram import enums
from Script import script
import asyncio
import json
from collections import defaultdict
from pyrogram import Client

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

#main variables
API_ID = int(environ.get('API_ID', ''))
API_HASH = environ.get('API_HASH', '')
BOT_TOKEN = environ.get('BOT_TOKEN', '')
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '').split()]
USERNAME = environ.get('USERNAME', 'https://telegram.me/ipopcornbotnews')
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', ''))
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '').split()]
DATABASE_URI = environ.get('DATABASE_URI', "")
DATABASE_URI2 = environ.get('DATABASE_URI2', "")
DATABASE_NAME = environ.get('DATABASE_NAME', "Rahul")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Rahul')
LOG_API_CHANNEL = int(environ.get('LOG_API_CHANNEL', '-1002339199841'))
QR_CODE = environ.get('QR_CODE', 'https://vault.pictures/media/images/94/f1/78/94f178a2c7844ce2aad6dedcc422bc57.png')
DELETE_CHANNELS = [int(dch) if id_pattern.search(dch) else dch for dch in environ.get('DELETE_CHANNELS', '0').split()]

#this vars is for when heroku or koyeb acc get banned, then change this vars as your file to link bot name
BIN_CHANNEL = int(environ.get('BIN_CHANNEL', ''))
URL = environ.get('URL', '')

# verify system vars
IS_VERIFY = is_enabled('IS_VERIFY', True)
LOG_VR_CHANNEL = int(environ.get('LOG_VR_CHANNEL', '1002339199841'))
TUTORIAL = environ.get("TUTORIAL", "https://t.me/How_to_verify_links/7")
TUTORIAL2 = environ.get("TUTORIAL2", "https://t.me/How_to_verify_links/8")
TUTORIAL3 = environ.get("TUTORIAL3", "https://t.me/How_to_verify_links/4")
VERIFY_IMG = environ.get("VERIFY_IMG", "https://vault.pictures/media/images/9a/4d/c4/9a4dc4b1ee1942319bd898a3ab0aa2ca.png")
SHORTENER_API = environ.get("SHORTENER_API", "312dabb23295e50b56e936144c740e2ab02c3b45")
SHORTENER_WEBSITE = environ.get("SHORTENER_WEBSITE", "shortner.in")
SHORTENER_API2 = environ.get("SHORTENER_API2", "86b2818c135d6d77b744e23e52f5e647efc3ebc1")
SHORTENER_WEBSITE2 = environ.get("SHORTENER_WEBSITE2", "indiaearnx.com")
SHORTENER_API3 = environ.get("SHORTENER_API3", "563704432490b9a58e574bbfb3585449420c2e2d")
SHORTENER_WEBSITE3 = environ.get("SHORTENER_WEBSITE3", "modijiurl.com")
TWO_VERIFY_GAP = int(environ.get('TWO_VERIFY_GAP', "3600"))
THREE_VERIFY_GAP = int(environ.get('THREE_VERIFY_GAP', "21600"))

# languages search
LANGUAGES = ["hindi", "english", "telugu", "tamil", "kannada", "malayalam"]

auth_channel = environ.get('AUTH_CHANNEL', '')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
SUPPORT_GROUP = int(environ.get('SUPPORT_GROUP', 'https://telegram.me/iPopcornbotNews'))

# bot settings
AUTO_FILTER = is_enabled('AUTO_FILTER', True)
PORT = os.environ.get('PORT', '8080')
MAX_BTN = int(environ.get('MAX_BTN', '8'))
AUTO_DELETE = is_enabled('AUTO_DELETE', True)
DELETE_TIME = int(environ.get('DELETE_TIME', 600))
IMDB = is_enabled('IMDB', False)
FILE_CAPTION = environ.get('FILE_CAPTION', f'{script.FILE_CAPTION}')
IMDB_TEMPLATE = environ.get('IMDB_TEMPLATE', f'{script.IMDB_TEMPLATE_TXT}')
LONG_IMDB_DESCRIPTION = is_enabled('LONG_IMDB_DESCRIPTION', False)
PROTECT_CONTENT = is_enabled('PROTECT_CONTENT', False)
SPELL_CHECK = is_enabled('SPELL_CHECK', True)
LINK_MODE = is_enabled('LINK_MODE', True)
PM_SEARCH = is_enabled('PM_SEARCH', True)
