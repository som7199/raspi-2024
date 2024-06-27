import RPi.GPIO as GPIO
import time

# 0 ~ 9까지 1byte hex값
#fndDatas = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x27, 0x7f, 0x6f]	# Cathode
fndDatas = [0xC0, 0xF9, 0xA4, 0xB0, 0x99, 0x92, 0x82, 0xD8, 0x80, 0x90]	# Anode
# a ~ g led
fndSegs = [5, 6, 12, 16, 20, 13, 21]
# fnd 선택 pin
#fndSels = [18, 22, 23, 24]
# [com4, com3, com2, com1]이 되도록 변경!
fndSels = [24, 23, 22, 18]
count = 0

GPIO.setmode(GPIO.BCM)
for fndSeg in fndSegs:
	GPIO.setup(fndSeg, GPIO.OUT)
	GPIO.output(fndSeg, 1)

for fndSel in fndSels:
	GPIO.setup(fndSel, GPIO.OUT)
	GPIO.output(fndSel, 0)

# 하나의 숫자 형태를 만드는 함수
def fndOut(data, sel):
	for _ in range(0, 50):
		for i in range(0, 7):
			# 비트 AND 연산으로 특정 세그먼트가 켜져 있는지 확인
			GPIO.output(fndSegs[i], fndDatas[data] & (0x01 << i))
			# 표시할 자리수의 fnd만 ON
			for j in range(0, 4):
				if j == sel:
					GPIO.output(fndSels[j], 1)
				else:
					GPIO.output(fndSels[j], 0)


try:
	while True:
		count += 1
		if count > 9999:
			count = 0
		d1000 = count / 1000
		d100 = count % 1000 / 100
		d10 = count % 100 / 10
		d1 = count % 10

		d = [d1, d10, d100, d1000]

		for i in range(3, -1, -1):	# fnd 선택 for문
			fndOut(int(d[i]), i)			# 값과 자리수 전달
			time.sleep(0.003)

except KeyboardInterrupt:
	GPIO.cleanup()
