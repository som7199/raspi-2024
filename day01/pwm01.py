#피에조
import RPi.GPIO as GPIO
import time

piezoPin = 13		# +에 연결
melody = [130, 147, 165, 175, 196, 220, 247, 262]

GPIO.setmode(GPIO.BCM)
GPIO.setup(piezoPin, GPIO.OUT)

# 아날로그 출력을 위한 객체 생성(440HZ 출력)
# piezoPin에 440HZ의 아날로그 출력이 일어남
# Pulse Width Modulation, 폭에 따른 제어!
Buzz = GPIO.PWM(piezoPin, 440)

try:
	while True:
		Buzz.start(50)	# Duty cycle 50(on 되는 시간) 가짐
		for i in range(0, len(melody)):
			Buzz.ChangeFrequency(melody[i])
			time.sleep(0.3)
		Buzz.stop()
		time.sleep(1)

except KeyboardInterrupt:
	GPIO.cleanup()
