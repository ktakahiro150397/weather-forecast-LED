#timeモジュールをインポート
import asyncio
import time

#RPi.GPIOモジュールをインポート
import RPi.GPIO as GPIO

from LEDEmitter import LEDEmmitter

async def main():
        
    # BCM(GPIO番号)で指定する設定
    GPIO.setmode(GPIO.BCM)

    try:
        gpio_17 = LEDEmmitter(17)
        gpio_27 = LEDEmmitter(27)

        loopCount = 1
        while True:
            print(f"{loopCount} : mainloop_begin")

            # # GPIO17の出力を1にして、LED点灯
            # gpio_17.LED_On()

            # # 0.5秒待つ
            # time.sleep(0.5)

            # # GPIO17の出力を0にして、LED消灯
            # gpio_17.LED_Off()

            # # 0.5秒待つ
            # time.sleep(0.5)

            # await gpio_17.Blink(500)
            # await gpio_27.Blink(500)
            blinkTask = [gpio_17.Blink(500),gpio_27.Blink(500)]
            await asyncio.gather(*blinkTask)

            # await asyncio.sleep(1)

            print(f"{loopCount} : mainloop_end")
            loopCount += 1

    except KeyboardInterrupt:
        # GPIO設定クリア
        GPIO.cleanup()



if __name__ == "__main__":
    asyncio.run(main())