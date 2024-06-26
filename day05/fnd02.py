import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정
segment_pins = [5, 6, 12, 16, 20, 13, 21]
switch = 17

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
	GPIO.setup(switch, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
	for pin in segment_pins:
		GPIO.setup(pin, GPIO.OUT)

def display_number(number):
	pattern = segment_patterns[number]
	for pin, state in zip(segment_pins, pattern):
		GPIO.output(pin, state)
		#print(pin, state)
	#print()

def main():
	try:
		setup()
		i = 0
		while True:
			if i > 9:
				i = 0
			if GPIO.input(switch):
				display_number(i)
				time.sleep(1)
				i += 1

	except KeyboardInterrupt:
		print("")
	finally:
		GPIO.cleanup()

if __name__ == '__main__':
	main()
