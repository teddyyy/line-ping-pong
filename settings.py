# -*- coding: utf-8 -*-

import os
import sys
import yaml
from linebot import LineBotApi, WebhookHandler

REPLY_PATH = './config/reply.yml'
ECHO_PATH = './config/echo.yml'

# LINE
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)

if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# reply words
reply_words = []
with open(REPLY_PATH, 'r', encoding='utf-8') as f:
    text = f.read()
    reply_words = yaml.load(text)

# echo words
echo_words = {}
with open(ECHO_PATH, 'r', encoding='utf-8') as f:
    text = f.read()
    echo_words = yaml.load(text)
