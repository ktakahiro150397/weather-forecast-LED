# -*- coding: utf-8 -*-

#timeモジュールをインポート
import asyncio
from datetime import datetime, timedelta, timezone
import json
from logging import config,getLogger
import os
import time
import traceback
import discord_send
from dotenv import load_dotenv

#RPi.GPIOモジュールをインポート
import RPi.GPIO as GPIO

from LEDEmitter import LEDEmmitter
from WeatherForecast.GetWeatherInformation import GetWeatherInformation,WeatherPoint
from WeatherInfoEmitDecision import WeatherInfoEmitDecision

# 環境変数を読み込み
load_dotenv()

# 現在のスクリプトファイルの絶対パスを取得する
script_dir = os.path.dirname(os.path.abspath(__file__))

# 設定ファイルのパスを作成する
settings_file_path = os.path.join(script_dir, "logsettings.json")

# ログ設定読込
with open(settings_file_path) as f:
    config.dictConfig(json.load(f))
logger = getLogger(__name__)

# 天気情報の取得間隔
WEATHER_INFO_RETRIEVE_INTERVAL_MIN : int = 30

weatherInfo = GetWeatherInformation("9d95720fc98f0ba079feff3a81ac2408")
blinkDecision = WeatherInfoEmitDecision()

async def main():
        
    # BCM(GPIO番号)で指定する設定
    GPIO.setmode(GPIO.BCM)

    try:
        gpio_17 = LEDEmmitter(17)
        gpio_27 = LEDEmmitter(27)

        # 前回情報取得日時 最大時刻で初期化(初回で取得するため)
        previous_retrive_date = datetime.max

        # 点滅するかどうか
        isBlink = False

        while True:
            shouldRetrieveWeatherInfo = False

            # 天気情報を取得するかどうかを確認
            delta = datetime.now() - previous_retrive_date
            if delta.seconds > WEATHER_INFO_RETRIEVE_INTERVAL_MIN * 60:
                # 指定分より時間が経過している
                logger.debug("OpenWeatherMapからデータを取得します。")
                shouldRetrieveWeatherInfo = True
                previous_retrive_date = datetime.now()

            if shouldRetrieveWeatherInfo:
                info = weatherInfo.getWeather(WeatherPoint.WeatherPoint.AKASHI)
                logger.debug("OpenWeatherMapからデータを取得しました。")
                logger.debug(info)

                # 点滅するかどうかを判定
                isBlink = blinkDecision.isBlink(info)
                if isBlink :
                    logger.debug("LEDを点滅させます。")
                else:
                    logger.debug("LEDを点滅させません。")

            if isBlink:
                blinkTask = [gpio_17.Blink(500)]
                await asyncio.gather(*blinkTask)



    except KeyboardInterrupt:
        # GPIO設定クリア
        GPIO.cleanup()
    except Exception as ex:
        GPIO.cleanup()
        logger.debug(ex)

        # エラー内容をDiscordに送信
        author = discord_send.discord_send_author(name="weather-forecast.py エラー通知",
                                                  icon_url="")
        webhookUrl = os.getenv("DISCORD_SEND_URL")
        sender = discord_send.discord_sender(webhookUrl)

        sender.sendExceptionMessage(author,ex)

if __name__ == "__main__":
    asyncio.run(main())