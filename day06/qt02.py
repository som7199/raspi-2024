import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

# Qt Designer로 만든 .ui 파일을 파이썬 코드에서 사용할 수 있도록 변환
form_class = uic.loadUiType("./btn01.ui")[0]

# windowClass
class WindowClass(QMainWindow, form_class):
	def __init__(self):					# 생성자, 첫 번째 인자는 self
		super().__init__()				# 부모 클래스 생성자(QWidget)
		self.setupUi(self)

		# 이벤트 함수 등록
		self.btn_1.clicked.connect(self.btn1Function)
		self.btn_2.clicked.connect(self.btn2Function)

	def btn1Function(self):
		print("LED ON Button Clicked")

	def btn2Function(self):
		print("LED OFF Button Clicked")

	# Qt Designer에서 만든 EXIT(btn_3)에 연결된 slot()
	# Qt Designer에서 제공하는 Edit slot 기능을 쓰면 위의 btn_1, btn_2처럼
	# 이벤트 함수 등록을 따로 안해줘도 됨!
	def btn3Func(self):
		print("EXIT")

if __name__ == "__main__":
	app = QApplication(sys.argv)	# 프로그램 실행시키는 클래스
	myWindow = WindowClass()			# WindowClass() 인스턴스 생성
	myWindow.show()								# 화면 보여주기
	app.exec_()										# 프로그램 실행
