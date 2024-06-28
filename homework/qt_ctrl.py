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

		#self.rdoPiezo.clicked.connect(self.rdoPiezoOnFunction)
		self.rdoPiezo.toggled.connect(self.rdoPiezoToggleFunction)
		self.ultraBtn.clicked.connect(self.ultraBtnFunction)

		self.piezo_thread = None			# 피에조 부저 제어 스레드
		self.piezo_running = False		# 피에조 부저의 동작 여부 제어 플래그

	def ledRedOnFunction(self):
		self.lblInfo.setText("RED ON")
		GPIO.output(redPin, False)
		GPIO.output(bluePin, True)
		GPIO.output(greenPin, True)

	def ledGreenOnFunction(self):
		self.lblInfo.setText("GREEN ON")
		GPIO.output(redPin, True)
		GPIO.output(greenPin, False)
		GPIO.output(bluePin, True)

	def ledBlueOnFunction(self):
		self.lblInfo.setText("BLUE ON")
		GPIO.output(redPin, True)
		GPIO.output(greenPin, True)
		GPIO.output(bluePin, False)

	def ledOffFunction(self):
		self.lblInfo.setText("LED OFF")
		GPIO.output(redPin, True)
		GPIO.output(bluePin, True)
		GPIO.output(greenPin, True)

	def rdoPiezoOnFunction(self):
		self.piezo_running = True
		self.lblInfo.setText("Buzzor ON!")
		self.pwm = GPIO.PWM(piezoPin, 440)
		self.pwm.start(90.0)

		#[0도, 1, 2, 3, 4솔, 5, 6, 7]
		scale = [262, 294, 330, 349, 392, 440, 494, 523]
		#scale = [262, 330]
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
		#self.lblInfo.setText("Buzzor OFF!")
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


	# TODO : ultraBtn 클릭하면 lcdNumber에 거리 띄우기
	# distance < 20일 경우 빨간불/경고음 발생
	def ultraBtnFunction(self):
		self.lblDist.setText("Start measuring!")
		count = 0
		print("Start Checking Distance!")
		while count <= 50:
			self.lcdNumber.display(count)
			count += 1

if __name__ == "__main__":
	app = QApplication(sys.argv)
	myWindow = WindowClass()
	myWindow.show()
	app.exec_()
