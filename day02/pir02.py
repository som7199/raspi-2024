import RPi.GPIO as GPIO
import time

pirPin = 24
led = 21

GPIO.setmode(GPIO.BCM)
# GPIO.setup(pirPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
# 해당 핀의 풀다운 저항을 활성화
# 풀다운 저항을 활성화하면 핀이 부동 상태일 때(센서가 신호를 보내지 않을 때) 핀의 상태가 기본적으로 LOW(0)가 됨
GPIO.setup(pirPin, GPIO.IN)
GPIO.setup(led, GPIO.OUT)

try:
	while True:
		# 감지되면 LED ON
		if GPIO.input(pirPin) == False:
			print("Detected!")
			GPIO.output(led, False)
			time.sleep(1)
		else:
			print("Undetected")
			GPIO.output(led, True)
			time.sleep(1)
except KeyboardInterrupt:
	GPIO.cleanup()
