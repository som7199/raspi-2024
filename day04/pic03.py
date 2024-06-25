from picamera2 import Picamera2
import RPi.GPIO as GPIO
import time
import datetime

swPin = 6
oldSw = 0
newSw = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(swPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start()

try:
	while True:
		newSw = GPIO.input(swPin)
		if newSw != oldSw:
			oldSw = newSw

			if newSw == 1:
				now = datetime.datetime.now()
				print(now)
				fileName = now.strftime('%Y-%m-%d %H:%M:%S')
				picam2.capture_file(fileName + '.jpg')

			time.sleep(0.2)

except KeyboardInterrupt:
	pass
