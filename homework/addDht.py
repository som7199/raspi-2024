import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QTimer, pyqtSignal, QThread
import RPi.GPIO as GPIO
import Adafruit_DHT
import time

redPin = 17
greenPin = 27
bluePin = 19
trigPin = 24
echoPin = 23
pirPin = 22
piezoPin = 13
dhtPin = 4  # DHT11 센서 핀 번호

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # 경고 메시지 비활성화
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
class DistanceMeasurementThread(QThread):
    update_distance_signal = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.running = False
        self.pwm = None

    def run(self):
        self.pwm = GPIO.PWM(piezoPin, 440)
        self.pwm.start(0)
        while self.running:
            distance = self.measure()
            self.update_distance_signal.emit(distance)
            self.controlWarning(distance)
            time.sleep(0.5)

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
            self.pwm.ChangeDutyCycle(0)
            time.sleep(1)

    def measure(self):
        GPIO.output(trigPin, True)
        time.sleep(0.00001)
        GPIO.output(trigPin, False)
        start = time.time()

        while GPIO.input(echoPin) == False:
            start = time.time()

        while GPIO.input(echoPin) == True:
            stop = time.time()

        elapsed = stop - start
        distance = (elapsed * 19000) / 2
        return int(distance)

    def stop(self):
        self.running = False
        self.wait()
        self.pwm.stop()
        GPIO.output(redPin, True)
        GPIO.output(greenPin, True)
        GPIO.output(bluePin, True)

# 온습도 측정 스레드 클래스 - QThread 상속
class DHTMeasurementThread(QThread):
    update_temperature_signal = pyqtSignal(float)
    update_humidity_signal = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.running = False

    def run(self):
        while self.running:
            humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, dhtPin)
            if humidity is not None and temperature is not None:
                self.update_temperature_signal.emit(temperature)
                self.update_humidity_signal.emit(humidity)
            time.sleep(2)

    def stop(self):
        self.running = False
        self.wait()

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

        self.piezo_thread = None
        self.piezo_running = False

        self.measurement_thread = DistanceMeasurementThread()
        self.measurement_thread.update_distance_signal.connect(self.updateLcdNumber)

        self.dht_thread = DHTMeasurementThread()
        self.dht_thread.update_temperature_signal.connect(self.updateTemperature)
        self.dht_thread.update_humidity_signal.connect(self.updateHumidity)
        self.dht_thread.running = True
        self.dht_thread.start()  # 온습도 측정 스레드 시작

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
            GPIO.output(redPin, False)
            GPIO.output(greenPin, True)
            GPIO.output(bluePin, True)
        elif distance <= 10:
            self.lblWarning.setText("Watch out!")
            self.lblWarning.setStyleSheet("color : green")
            GPIO.output(redPin, True)
            GPIO.output(greenPin, False)
            GPIO.output(bluePin, True)
        elif distance <= 15:
            self.lblWarning.setText("Caution!")
            self.lblWarning.setStyleSheet("color : blue")
            GPIO.output(redPin, True)
            GPIO.output(greenPin, True)
            GPIO.output(bluePin, False)
        else:
            self.lblWarning.setText("")
            GPIO.output(redPin, True)
            GPIO.output(greenPin, True)
            GPIO.output(bluePin, True)

    def updateTemperature(self, temperature):
        self.lcdNumberTemp.display(temperature)

    def updateHumidity(self, humidity):
        self.lcdNumberHum.display(humidity)

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
