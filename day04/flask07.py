# 동일한 폴더 위치에 templates 폴더를 만든 후 html 파일 저장

from flask import Flask, request, render_template
#from gpiozero import LED
import RPi.GPIO as GPIO

app = Flask(__name__)

#red_led = LED(20)
red_led = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(red_led, GPIO.OUT)

@app.route('/')
def home():
	return render_template("index.html")

@app.route('/data', methods = ['POST'])
def data():
	data = request.form['led']

	if data == 'on':
		#red_led.on()
		GPIO.output(red_led, False)
		return home()

	elif data == 'off':
		#red_led.off()
		GPIO.output(red_led, True)
		return home()

if __name__ == '__main__':
	app.run(host='0.0.0.0', port='18080', debug=True)
