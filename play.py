from pydub import AudioSegment
from pydub.playback import play
import os, sys, json

from linebot import LineBotApi
from linebot.models import TextSendMessage

from flask import Flask, request, abort
 
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

channel_access_token = os.getenv('')

line_user_ids = os.getenv('').split(',')
line_bot_api = LineBotApi(channel_access_token)