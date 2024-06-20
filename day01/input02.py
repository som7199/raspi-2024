import RPi.GPIO as GPIO
import time

led = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)

try:
	while True:
		chr = input("LED ON > O | LED OFF > X : ")
		if chr == "O":
			GPIO.output(led, False)
			print("LED ON!\n")
		if chr == "X":
			GPIO.output(led, True)
			print("LED OFF!\n")
except KeyboardInterrupt:
	GPIO.cleanup()
