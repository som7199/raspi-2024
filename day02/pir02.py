import RPi.GPIO as GPIO
import time

pirPin = 24
led = 21

GPIO.setmode(GPIO.BCM)
#GPIO.setup(pirPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
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
