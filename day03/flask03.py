# URL 접속을 /led/on, /led/off로 접속하면 led를 on, off 하는 웹페이지 만들기
from flask import Flask
import RPi.GPIO as GPIO

app = Flask(__name__)
led = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)

@app.route("/")
def hello():
	return "Hello World"

@app.route("/led/on")
def ledOn():
	GPIO.output(led, False)
	return "<h1>LED ON!</h1>"

@app.route("/led/off")
def ledOff():
	GPIO.output(led, True)
	return "<h1>LED OFF!</h1>"

if __name__ == "__main__":
	app.run(host="0.0.0.0", port="18080", debug=True)
	if KeyboardInterrupt:
		GPIO.cleanup()
