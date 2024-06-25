#from gpiozero import Button
import RPi.GPIO as GPIO
import time

#swPin = Button(6)
swPin = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(swPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

oldSw = 0
newSw = 0

try:
	while True:
		#newSw = swPin.is_pressed
		newSw = GPIO.input(swPin)
		if newSw != oldSw:
			oldSw = newSw

			if newSw == 1:
				print("click")

			time.sleep(0.2)

except KeyboardInterrupt:
	pass
