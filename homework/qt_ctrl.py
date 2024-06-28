import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import RPi.GPIO as GPIO
import time

redPin = 17
greenPin = 27
bluePin = 19
led = [redPin, greenPin, bluePin]

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
		for i in range(len(led)):
			self.led[i].clicked.connect(self.ledBtnOffFunction)

		self.ledRed.clicked.connect(self.ledRedOnFunction)
		self.ledGreen.clicked.connect(self.ledGreenOnFunction)
		self.ledBlue.clicked.connect(self.ledBlueOnFunction)

		self.ultraBtn.clicked.connect(self.ultraBtnFunction)

	def ledRedOnFunction(self):
		GPIO.output(redPin, False)
		GPIO.output(bluePin, True)
		GPIO.output(greenPin, True)

	def ledGreenOnFunction(self):
		GPIO.output(redPin, True)
		GPIO.output(greenPin, False)
		GPIO.output(bluePin, True)

	def ledBlueOnFunction(self):
		GPIO.output(redPin, True)
		GPIO.output(greenPin, True)
		GPIO.output(bluePin, False)

	def ledBtnOffFunction(self):
		GPIO.output(redPin, True)
		GPIO.output(bluePin, True)
		GPIO.output(greenPin, True)

	# TODO : ultraBtn 클릭하면 ultraLabel.Text에 거리 띄워지게 하기
	# 세그먼트에 거리 띄우기
	def ultraBtnFunction(self):
		count = 0
		print("Ultra Button Clicked!\nStart Checking Distance!")
		while count < 50:
			#self.ultraLabel.text = count
			count += 1

if __name__ == "__main__":
	app = QApplication(sys.argv)
	myWindow = WindowClass()
	myWindow.show()
	app.exec_()
