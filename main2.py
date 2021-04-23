from pydub import AudioSegment
from pydub.playback import play

import os
import sys
import json

import RPi.GPIO as GPIO # RPi.GPIOモジュールを使用

import time


audio = os.listdir("midnightEXP")

print(audio)

AudioData = {}

# ngrokのURL末尾には/callbackをつけること

for i in audio:
    if i[-3:] != "mp3":
        print("ダメ")
        continue

    AudioData[i.replace(".mp3", "")] = AudioSegment.from_mp3(os.path.join("midnightEXP", i))

counter = 0

GPIO.setmode(GPIO.BCM)  #GPIOへアクセスする番号をBCMの番号で指定することを宣言します。                        
GPIO.setup(2,GPIO.IN)   #BCM 2番ピンを入力に設定します。                                                      

flag = True

try:
        while True:
                if GPIO.input(2) == GPIO.HIGH and flag:

                    flag = False

                    print("再生",counter)

                    #play(AudioData[str(counter)])
                    
                    counter += 1

                    time.sleep(3)

                    flag = True

                
                    
except KeyboardInterrupt:
        GPIO.cleanup()
