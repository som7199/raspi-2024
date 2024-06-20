import RPi.GPIO as GPIO
import time

led = 21

# GPIO 핀번호 설정 (BCM 모드)
GPIO.setmode(GPIO.BCM)
# GPIO 핀설정 (출력모드)
GPIO.setup(led, GPIO.OUT)

try:
    while True:
        GPIO.output(led, True)  # LED 켜기
        time.sleep(1)           # 1초 대기
        GPIO.output(led, False) # LED 켜기
        time.sleep(1)           # 1초 대기

except KeyboardInterrupt:  # Ctrl + C
    GPIO.output(led, False) # LED 끄기
    GPIO.cleanup()          # GPIO 설정
