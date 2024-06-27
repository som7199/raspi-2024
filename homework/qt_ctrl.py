import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import RPi.GPIO as GPIO

red = 4
green = 17
blue = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

form_class = uic.loadUiType("./homework.ui")[0]

class WindowClass(QMainWindow, form_class):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

		# 이벤트 함수 등록
		self.ledBtnOn.clicked.connect(self.ledBtnOnFunction)
		self.ledBtnOff.clicked.connect(self.ledBtnOffFunction)
		self.ultraBtn.clicked.connect(self.ultraBtnFunction)

	def ledBtnOnFunction(self):
		GPIO.output(red, False)

	def ledBtnOffFunction(self):
		GPIO.output(red, True)

	# TODO : ultraBtn 클릭하면 ultraLabel.Text에 거리 띄워지게 하기
	# 어라 세그먼트에 거리 띄우기로 바꿀래
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
