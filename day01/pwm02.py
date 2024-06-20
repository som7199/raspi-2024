import RPi.GPIO as GPIO
import time

piezoPin = 13
melody = [130, 147, 165, 175, 196, 220, 247, 262]
GPIO.setmode(GPIO.BCM)
GPIO.setup(piezoPin, GPIO.OUT)

Buzz = GPIO.PWM(piezoPin, 440)

try:
	while True:
		chr = int(input("도(1) ~ 8(도), 종료는 9 > "))
		if chr in range(1, 9):
			Buzz.start(25)
			Buzz.ChangeFrequency(melody[chr - 1])
			time.sleep(0.5)
			Buzz.stop()
		elif chr == 9:
			Buzz.stop()
except KeyboardInterrupt:
	GPIO.cleanup()
