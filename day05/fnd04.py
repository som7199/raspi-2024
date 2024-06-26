# 0 ~ 9999 출력하기
# 11, 22, ~, 99 / 111, 222, ~, 999 / 1111, 2222, ~, 9999로 출력되는 중...
# 순서대로 1 ~ 10, 11, 12, ~ 9999까지 출력되는 코드는 fnd04_m.py
import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정
segment_pins = [5, 6, 12, 16, 20, 13, 21]
com_pins = [18, 22, 23, 24]

# 각 숫자에 해당하는 7세그먼트 패턴 (0 ~ 9)
segment_patterns = [
    [0, 0, 0, 0, 0, 0, 1],  # 0
    [1, 0, 0, 1, 1, 1, 1],  # 1
    [0, 0, 1, 0, 0, 1, 0],  # 2
    [0, 0, 0, 0, 1, 1, 0],  # 3
    [1, 0, 0, 1, 1, 0, 0],  # 4
    [0, 1, 0, 0, 1, 0, 0],  # 5
    [0, 1, 0, 0, 0, 0, 0],  # 6
    [0, 0, 0, 1, 1, 1, 1],  # 7
    [0, 0, 0, 0, 0, 0, 0],  # 8
    [0, 0, 0, 0, 1, 0, 0]   # 9
]

def setup():
	GPIO.setmode(GPIO.BCM)
	for pin in segment_pins:
		GPIO.setup(pin, GPIO.OUT)

	for com in com_pins:
		GPIO.setup(com, GPIO.OUT)

def display_number(pos, number):
	pattern = segment_patterns[number]

	for i in range(len(com_pins)):
		if i == pos:
			GPIO.output(com_pins[i], True)
			for pin, state in zip(segment_pins, pattern):
				GPIO.output(pin, state)

def main():
	try:
		setup()
		while True:
			for i in range(len(com_pins)):
				GPIO.output(com_pins[i], False)

			for i in range(3, 0, -1):
				for j in range(1, 10):
					display_number(i, j)
					time.sleep(0.5)
				display_number(i, 0)
			time.sleep(1)

	except KeyboardInterrupt:
		GPIO.cleanup()

if __name__ == '__main__':
	main()
