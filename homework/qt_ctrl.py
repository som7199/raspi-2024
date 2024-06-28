import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import RPi.GPIO as GPIO
import threading
import time

redPin = 17
greenPin = 27
bluePin = 19
trigPin = 24
echoPin = 23
pirPin = 22
piezoPin = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(bluePin, GPIO.OUT)
GPIO.setup(trigPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)
GPIO.setup(pirPin, GPIO.IN)
GPIO.setup(piezoPin, GPIO.OUT)

form_class = uic.loadUiType("./homework.ui")[0]

class WindowClass(QMainWindow, form_class):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

		# 이벤트 함수 등록
		self.ledRed.clicked.connect(self.ledRedOnFunction)
		self.ledGreen.clicked.connect(self.ledGreenOnFunction)
		self.ledBlue.clicked.connect(self.ledBlueOnFunction)
		self.ledOff.clicked.connect(self.ledOffFunction)

		self.rdoPiezo.toggled.connect(self.rdoPiezoToggleFunction)
		self.ultraStartBtn.clicked.connect(self.ultraStartBtnFunction)
		self.ultraStopBtn.clicked.connect(self.ultraStopBtnFunction)

		self.piezo_thread = None			# 피에조 부저 제어 스레드
		self.piezo_running = False		# 피에조 부저의 동작 여부 제어 플래그

	def ledRedOnFunction(self):
		self.lblLedInfo.setText("RED ON")
		GPIO.output(redPin, False)
		GPIO.output(bluePin, True)
		GPIO.output(greenPin, True)

	def ledGreenOnFunction(self):
		self.lblLedInfo.setText("GREEN ON")
		GPIO.output(redPin, True)
		GPIO.output(greenPin, False)
		GPIO.output(bluePin, True)

	def ledBlueOnFunction(self):
		self.lblLedInfo.setText("BLUE ON")
		GPIO.output(redPin, True)
		GPIO.output(greenPin, True)
		GPIO.output(bluePin, False)

	def ledOffFunction(self):
		self.lblLedInfo.setText("LED OFF")
		GPIO.output(redPin, True)
		GPIO.output(bluePin, True)
		GPIO.output(greenPin, True)

	def rdoPiezoOnFunction(self):
		self.piezo_running = True
		self.lblSound.setText("Buzzor ON!")
		self.pwm = GPIO.PWM(piezoPin, 440)
		self.pwm.start(90.0)

		#[0도, 1, 2, 3, 4솔, 5, 6, 7]
		scale = [262, 294, 330, 349, 392, 440, 494, 523]
		melody = [0, 0, 4, 4, 5, 5, 4, 3, 3, 2, 2, 1, 1, 0]

		while self.piezo_running:
			for i in range(len(melody)):
				if not self.piezo_running:
					break
				if i == 6:
					self.pwm.ChangeFrequency(scale[melody[i]])
					time.sleep(1)
				else:
					self.pwm.ChangeFrequency(scale[melody[i]])
					time.sleep(0.5)

	def rdoPiezoOffFunction(self):
		self.piezo_running = False
		self.lblSound.setText("Buzzor OFF!")
		if self.pwm is not None:
			self.pwm.stop()
			self.pwm = None

	def rdoPiezoToggleFunction(self):
		if self.rdoPiezo.isChecked():
			if self.piezo_thread is None or not self.piezo_thread.is_alive():
				self.piezo_thread = threading.Thread(target=self.rdoPiezoOnFunction)
				self.piezo_thread.start()
		else:
			self.rdoPiezoOffFunction()

	def measure(self):
		GPIO.output(trigPin, True)		# 10us 동안 high 레벨로 trigger 출력하여 초음파 발생 준비
		time.sleep(0.00001)
		GPIO.output(trigPin, False)
		start = time.time()							# 현재 시간 저장

		while GPIO.input(echoPin) == False:		# echo가 없으면
			start = time.time()									# 현재 시간을 start 변수에 저장하고

		while GPIO.input(echoPin) == True:		# echo가 있으면
			stop = time.time()									# 현재 시간을 stop 변수에 저장

		dlapsed = stop - start								# 걸린 시간을 구하고
		distance = (dlapsed * 19000) / 2			# 초음파 속도를 이용해서 거리 계산
		return distance

	# TO-DO
	# ultraBtn 클릭하면 lcdNumber에 거리 띄우기
	# 거리가 5 이하일 때 Too Close label 활성화
	# ultraStopBtnFunction() 구현
	# 온습도센서 구현
	def ultraStartBtnFunction(self):
		self.lblDist.setText("Start measuring!")
		self.pwm = GPIO.PWM(piezoPin, 440)

		while True:
			distance = self.measure()
			print("Distance : %2.f cm" %distance)
			self.lcdNumber.display(distance)

			GPIO.output(redPin, True)
			GPIO.output(greenPin, True)
			GPIO.output(bluePin, True)

			if distance <= 5:
				self.pwm.start(50)
				self.pwm.ChangeFrequency(200)
				time.sleep(0.1)
				GPIO.output(redPin, False)
				GPIO.output(greenPin, True)
				GPIO.output(bluePin, True)
				self.pwm.ChangeFrequency(400)
				time.sleep(0.1)

			elif distance <= 10:
				self.pwm.ChangeFrequency(300)
				time.sleep(0.3)
				GPIO.output(redPin, True)
				GPIO.output(greenPin, False)
				GPIO.output(bluePin, True)
				time.sleep(0.3)

			elif distance <= 20:
				self.pwm.ChangeFrequency(400)
				GPIO.output(redPin, True)
				GPIO.output(greenPin, True)
				GPIO.output(bluePin, False)
				time.sleep(0.6)

			else:
				self.pwm.stop()
				GPIO.output(redPin, True)
				GPIO.output(greenPin, True)
				GPIO.output(bluePin, True)
				time.sleep(1)

	def ultraStopBtnFunction(self):
		print("HI")

if __name__ == "__main__":
	app = QApplication(sys.argv)
	myWindow = WindowClass()
	myWindow.show()
	app.exec_()
