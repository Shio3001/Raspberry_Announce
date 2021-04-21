from pydub import AudioSegment
from pydub.playback import play
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
    return "open"


@app.route("/callback", methods=['POST'])
def callback():
    print("コールバック")

    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("InvalidSignatureError")
        abort(200)
    return 'OK'

# メッセージに反応


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
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
