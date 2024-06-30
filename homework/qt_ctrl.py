import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QThread
import RPi.GPIO as GPIO
import threading
import time
#import Adafruit_DHT

redPin = 17
greenPin = 27
bluePin = 19
trigPin = 24
echoPin = 23
pirPin = 22
piezoPin = 13
#dhtPin = 18
#dhtSensor = Adafruit_DHT.DHT11

GPIO.setmode(GPIO.BCM)
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(bluePin, GPIO.OUT)
GPIO.setup(trigPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)
GPIO.setup(pirPin, GPIO.IN)
GPIO.setup(piezoPin, GPIO.OUT)
GPIO.setup(dhtPin, GPIO.IN)

form_class = uic.loadUiType("./homework.ui")[0]

# 초음파 측정 스레드 클래스 - QThread 상속
# QThread 클래스를 이용해 별도의 스레드에서 초음파 측정
class DistanceMeasurementThread(QThread):
	# 측정 거리를 update_distance_signal 신호를 통해 메인 스레드로 전달
	update_distance_signal = pyqtSignal(float)

	def __init__(self):
		super().__init__()
		self.running = False
		self.pwm = None

	def run(self):
		self.pwm = GPIO.PWM(piezoPin, 440)
		self.pwm.start(0)		# 부저를 멈춘 상태로 시작
		while self.running:
			distance = self.measure()
			self.update_distance_signal.emit(distance)		# 신호 방출!
			self.controlWarning(distance)	# 부저 제어
			time.sleep(0.5)		# 측정 주기 조절

	def controlWarning(self, distance):
		if distance <= 5:
			self.pwm.ChangeDutyCycle(50)
			self.pwm.ChangeFrequency(200)
			time.sleep(0.1)
			self.pwm.ChangeFrequency(400)
			time.sleep(0.1)

		elif distance <= 10:
			self.pwm.ChangeDutyCycle(50)
			self.pwm.ChangeFrequency(100)
			time.sleep(0.3)
			self.pwm.ChangeFrequency(300)
			time.sleep(0.3)

		else:
			self.pwm.ChangeDutyCycle(0)		# 부저 멈추기
			time.sleep(1)

	def measure(self):
		# 10us 동안 high 레벨로 trigger 출력하여 초음파 발생 준비
		GPIO.output(trigPin, True)
		time.sleep(0.00001)
		GPIO.output(trigPin, False)
		# 현재 시간 저장
		start = time.time()

		# echo가 없으면
		while GPIO.input(echoPin) == False:
			start = time.time()

		# echo가 있으면
		while GPIO.input(echoPin) == True:
			stop = time.time()

		elapsed = stop - start							# 걸린 시간
		distance = (elapsed * 19000) / 2		# 초음파 속도를 이용한 거리 계산

		return int(distance)

	def stop(self):
		self.running = False
		self.wait()
		self.pwm.stop()
		GPIO.output(redPin, True)
		GPIO.output(greenPin, True)
		GPIO.output(bluePin, True)

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
		self.measurement_thread = DistanceMeasurementThread()	# 초음파 측정 스레드
		# 초음파 측정 스레드에서 발생하는 신호를 updateLcdNumber 함수에 연결
		self.measurement_thread.update_distance_signal.connect(self.updateLcdNumber)

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

	def updateLcdNumber(self, distance):
		self.lcdNumber.display(distance)
		if distance <= 5:
			self.lblWarning.setText("Too close!")
			self.lblWarning.setStyleSheet("color : red")
			time.sleep(0.1)
			GPIO.output(redPin, False)
			GPIO.output(greenPin, True)
			time.sleep(0.1)
			GPIO.output(redPin,True)
			time.sleep(0.1)
			GPIO.output(redPin, False)
			GPIO.output(greenPin, True)

		elif distance <= 10:
			self.lblWarning.setText("Watch out!")
			self.lblWarning.setStyleSheet("color : green")
			time.sleep(0.3)
			GPIO.output(redPin, True)
			GPIO.output(greenPin, False)
			time.sleep(0.3)
			GPIO.output(greenPin, True)
			time.sleep(0.3)
			GPIO.output(redPin, True)
			GPIO.output(greenPin, False)

		else:
			self.lblWarning.setText("")
			GPIO.output(redPin, True)
			GPIO.output(greenPin, True)

	def ultraStartBtnFunction(self):
		self.lblDist.setText("Start measuring!")
		self.measurement_thread.running = True
		self.measurement_thread.start()

	def ultraStopBtnFunction(self):
		self.lblDist.setText("Stop Measuring!")
		self.measurement_thread.stop()

if __name__ == "__main__":
	app = QApplication(sys.argv)
	myWindow = WindowClass()
	myWindow.show()
	app.exec_()
