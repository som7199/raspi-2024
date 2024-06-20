# raspi-2024
IoT 개발자 과정 라즈베리파이 리포지토리

## 1일차
- 키르히호프 법칙 
    - KVC(전압 법칙): 키르히호프 전압 법칙은 회로의 닫힌 루프에서 모든 전압 강하의 합이 0
    - KCL(전류 법칙): 키르히호프 전류 법칙은 회로의 임의의 접점에서 들어오는 전류의 합과 나가는 전류의 합이 같음
        ![KCL](https://raw.githubusercontent.com/som7199/raspi-2024/main/images/ras001.png)

- 전기회로 구조
    - 전류 ! : 모든 전류는 그라운드를 통해서 흐름 
    - 전압|볼트(V) : 전압은 전기 회로 내에서 전하가 이동하는 데 필요한 에너지 차이를 의미 , 전위차 또는 전기압이라고도 함
    - 저항|옴(Ω): 회로 내에서 전류의 흐름을 제어하고 조절하는 역할
        - 옴의 법칙 (Ohm's Law)
            - 전류 (I): 전하의 흐름, 단위는 암페어(A)
            - 전압 (V): 전하가 이동하는 데 필요한 에너지 차이, 단위는 볼트(V)
            - 저항 (R): 전류의 흐름을 방해하는 물질의 특성, 단위는 옴(Ω)

- GPIO 설정함수
    - GPIO.setmode(GPIO.BOARD) - wPi
    - GPIO.setmode(GPIO.BCM) - BCM
    - GPIO.setup(channel, GPIO.mode)
    - channel : 핀 번호, mode : IN/OUT
    - GPIO.cleanup()

- GPIO 출력함수
   - GPIO.output(channel , state)
    - channel : 핀 번호, state ; HIGH/LOW or 1/0 or True/Fasle
- GPIO 입력함수
   - GPIO.input(channel)
    - channel; 핀번호, 반환값 H/L or 1/- or T/F
- 시간지연 함수 TIME.SLEEP(SECS)

- VRGB
    - vcc : G , 에서 전류가 흘러옴 > 그라운드를 향해야 한바퀴를 돌아서 전류가 흐름 전원이 공급
    - R : Red색상을 켜기 위해선 R을 거쳐서 ground 로 향하면 됨 

- 스위치
    ![KCL](https://raw.githubusercontent.com/som7199/raspi-2024/main/images/ras002.png)