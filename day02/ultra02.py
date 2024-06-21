#Ultra
import RPi.GPIO as GPIO
import time

def measure():
	GPIO.output(triggerPin, True)		# 10us 동안 high 레벨로 trigger 출력하여 초음파 발생 준비
	time.sleep(0.00001)
	GPIO.output(triggerPin, False)
	start = time.time()							# 현재 시간 저장

	while GPIO.input(echoPin) == False:		# echo가 없으면
		start = time.time()									# 현재 시간을 start 변수에 저장하고

	while GPIO.input(echoPin) == True:		# echo가 있으면
		stop = time.time()									# 현재 시간을 stop 변수에 저장
	dlapsed = stop - start								# 걸린 시간을 구하고
	distance = (dlapsed * 19000) / 2			# 초음파 속도를 이용해서 거리 계산

	return distance												# 거리 반환

# 핀 설정
triggerPin = 24
echoPin = 23
piezoPin = 20
ledPin = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(triggerPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)
GPIO.setup(piezoPin, GPIO.OUT)
GPIO.setup(ledPin, GPIO.OUT)

Buzz = GPIO.PWM(piezoPin, 440)

try:
	while True:
		distance = measure()
		print("Distance : %.2f cm" %distance)
		if distance <= 5:
			Buzz.start(50)
			Buzz.ChangeFrequency(200)
			time.sleep(0.1)
			GPIO.output(ledPin, False)
			Buzz.ChangeFrequency(400)
			time.sleep(0.1)

		elif distance <= 10:
			Buzz.start(50)
			Buzz.ChangeFrequency(300)
			time.sleep(0.3)
			Buzz.stop()
			time.sleep(0.3)

		elif distance <= 20:
			Buzz.start(50)
			Buzz.ChangeFrequency(400)
			time.sleep(0.6)
			Buzz.stop()
			time.sleep(0.6)

		else:
			Buzz.stop()
			time.sleep(1)

		GPIO.output(ledPin, True)
except KeyboardInterrupt:
	GPIO.cleanup()
