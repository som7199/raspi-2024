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

GPIO.setmode(GPIO.BCM)
GPIO.setup(triggerPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)

try:
	while True:
		distance = measure()
		print("Distance : %.2f cm" %distance)
		time.sleep(1)

except KeyboardInterrupt:
	GPIO.cleanup()
