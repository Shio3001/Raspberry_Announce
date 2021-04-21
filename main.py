from pydub import AudioSegment
from pydub.playback import play

import simpleaudio

import os
import sys
import json

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
    MessageEvent, TextMessage, TextSendMessage, FollowEvent,
)

import datetime

print("http番号を入力")
http_number = int(input().rstrip())

audio = os.listdir("midnightEXP")

print(audio)

AudioData = {}

for i in audio:
    if i[-3:] != "mp3":
        print("ダメ")
        continue

    AudioData[i.replace(".mp3", "")] = AudioSegment.from_mp3(os.path.join("midnightEXP", i))


app = Flask(__name__)

# 環境変数取得
# LINE Developersで設定されているアクセストークンとChannel Secretをを取得し、設定します。

print(os.environ["CHANNEL_ACCESS_TOKEN"])
print(os.environ["CHANNEL_SECRET"])
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/")
def root():
    return str(datetime.datetime.now())


@app.route("/callback", methods=['POST'])
def callback():
    # リクエストヘッダーから署名検証のための値を取得します。
    signature = request.headers['X-Line-Signature']

    # リクエストボディを取得します。
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    # 署名を検証し、問題なければhandleに定義されている関数を呼び出す。
    try:
        handler.handle(body, signature)
    # 署名検証で失敗した場合、例外を出す。
    except InvalidSignatureError:
        abort(200)
    # handleの処理を終えればOK
    return 'OK'

# メッセージに反応


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    simpleaudio.stop_all()

    print("再生イベント")
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='再生'))
    play(AudioData[event.message.text])

# 友達追加イベントらしい


@handler.add(FollowEvent)  # これで受信して
def handle_follow(event):  # ラインAPIの返信機能関数に
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='特急ミッドナイトEXP松山 松山→新居浜'))


if __name__ == "__main__":
    print("起動する")
    port = int(os.getenv("PORT", http_number))
    app.run(host="0.0.0.0", port=port)
