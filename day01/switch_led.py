import RPi.GPIO as GPIO
import time

red = 4
green = 17
blue = 5
switch = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(switch, GPIO.IN)

i = 0
led = [red, green, blue]

try:
	while True:
		if GPIO.input(switch) == True:
			print("switch pushed!", end=" => ")

			if led[i % 3] == led[0]:
				GPIO.output(led[0], False)
				GPIO.output(led[1], True)
				GPIO.output(led[2], True)
				# GPIO.output(led[i % 3], False)
				print("red {} on!\n".format(led[i % 3]))
				time.sleep(0.5)
			if led[i % 3] == led[1]:
				GPIO.output(red, True)
				GPIO.output(green, False)
				GPIO.output(blue, True)
				print("green {} on!\n".format(led[i % 3]))
				time.sleep(0.5)
			if led[i % 3] == led[2]:
				GPIO.output(red, True)
				GPIO.output(green, True)
				GPIO.output(blue, False)
				print("blue {} on!\n".format(led[i % 3]))
				time.sleep(0.5)
			i += 1
except KeyboardInterrupt:
	GPIO.cleanup()
