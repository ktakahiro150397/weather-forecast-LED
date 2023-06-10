#RPi.GPIOモジュールをインポート
import asyncio
import time
import RPi.GPIO as GPIO

class LEDEmmitter():

    def __init__(self,gpio_number:int) -> None:
        GPIO.setmode(GPIO.BCM)

        # 指定されたピンを出力に変更
        GPIO.setup(gpio_number,GPIO.OUT)
        self.gpio_number = gpio_number

    def LED_On(self) -> None:
        GPIO.output(self.gpio_number,1)

    def LED_Off(self) -> None:
        GPIO.output(self.gpio_number,0)

    async def Blink(self,msec:int) -> None:
        blink_loop = asyncio.create_task(self._blink_loop(msec))
        await blink_loop

    async def _blink_loop(self,msec:int):
        self.LED_On()

        # 指定時間だけ待機
        await asyncio.sleep(msec/1000)

        self.LED_Off()

        # 指定時間だけ待機
        await asyncio.sleep(msec/1000)

