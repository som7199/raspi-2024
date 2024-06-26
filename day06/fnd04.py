import RPi.GPIO as GPIO
import time

# 0 ~ 9까지 1byte hex값
#fndDatas = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x27, 0x7f, 0x6f]	# Cathode
fndDatas = [0xC0, 0xF9, 0xA4, 0xB0, 0x99, 0x92, 0x82, 0xD8, 0x80, 0x90]	# Anode
# a ~ g led
fndSegs = [5, 6, 12, 16, 20, 13, 21]
# fnd 선택 pin
# fndSels = [24, 23, 22, 18]
fndSels = [24, 23, 22, 18]

GPIO.setmode(GPIO.BCM)
for fndSeg in fndSegs:
	GPIO.setup(fndSeg, GPIO.OUT)
	GPIO.output(fndSeg, 1)

for fndSel in fndSels:
	GPIO.setup(fndSel, GPIO.OUT)
	GPIO.output(fndSel, 0)

# 하나의 숫자 형태를 만드는 함수
def fndOut(data):
	for i in range(0, 7):
		GPIO.output(fndSegs[i], fndDatas[data] & (0x01 << i))

try:
	while True:
		for i in range(0, 4):
			GPIO.output(fndSels[i], 1)		# fnd 선택
			#GPIO.output(6, 0)
			#GPIO.output(12, 0)
			for j in range(0, 10):
				fndOut(5)		# 5 출력!
				time.sleep(0.5)

except KeyboardInterrupt:
	GPIO.cleanup()
