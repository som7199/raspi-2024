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
    - 내장 pull-down, pull-up 저항 사용
        - 스위치에 pull-down, pull-up 회로를 만들어주지 않고도 라즈베리파이 내부에 풀다운/풀업 저항을 만들어 놓고 sw로 활성화 할 수 있도록 되어있다.
        ```python
        GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP) # 스위치 안눌렸을 때 on, 눌렸을 때 off
        GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # 스위치 안눌렸을 때 off, 눌렸을 때 on
        ```
    ![input](https://raw.githubusercontent.com/som7199/raspi-2024/main/images/ras002.png)


- 피에조 부저(piezo buzzer) - PWM 방식으로 작동
    - (압전효과) 물체에 기계적인 압력을 가하면 전압이 발생하고 , 역으로 전압을 가하면 기계적인 변형이 발생하는 현상 
    - 디지털 핀의 전압을 매우 짧은 시간 안에 바꾸어가며 주파수에 맞는 소리를 낼 수 있음 
    - 능동 부저(Active Buzzer)
        - 외부 전원으로만 소리가 발생 **단순한 소리출력만 가능**
    - 수동 부저(Passive Buzzer)
        - 외부전기 신호를 받아서 소리를 발생시킴 
        - 능동부저와 다르게 **발진 회로가 없어 외부에서 제공되는 주파수 신호가 필요함**
        - 다양한 음색을 출력가능 
        - tone(), noTone()함수를 사용

        ![피에조 부저원리](https://raw.githubusercontent.com/som7199/raspi-2024/main/images/ras003.png)

## 2일차
- 가상환경에서 작업하기
    - python -m venv 가상환경 이름(rpiEnv로 함)
    - source ./rpiEnv/bin/activate 로 가상환경 실행
    - pip install RPi.GPIO로 필요한 패키지 설치
    - 가상환경을 빠져나오려면 decativate

- 가상환경 밖에서
    - sudo git clone https://github.com/WiringPi/WiringPi (raspi-2024/day02/ 에 클론..!)
    - cd WiringPi에서 sudo ./build 실행하고
    - gpio -v 로 확인해보기!

- 적외선 인체감지 센서(PIR, Passive Infrated Sensor)
    - 역할 : 센서는 적외선을 감지하여 움직임을 감지하는 센서
        - 핀 구성 3가지 
            - VCC: 전원 공급 핀(보통 5V 또는 3.3V)
            - GND: 접지 핀
            - OUT: 출력 핀 (감지 신호 출력)
        - 특징
            - 출력 신호: 디지털 출력 (High/Low 신호)
    - 감도조절
        - 모듈 앞에 노란색 조절기 돌리기 

- 초음파 센서 (HC-SR04 초음파 센서)
 - 초음파를 방출하고 반사되어 돌아오는 시간을 측정하여 거리를 계산 (약 40KHz)
 - 실내에서 측정할 경우 반사 물체가 너무 가깝거나 너무 멀리 있을 때 정확한 측정이 어려울 수 있음
    - 작동원리
        - 송신기 : 40KHz 영역대의 초음파를 방출 
        - 수신시 : 송신기에서 방출된 초음파가 물체에 반사되어 수신기에 돌아온 시간을 통해 거리를 측정
        
        ![초음파센서 작동원리](https://raw.githubusercontent.com/som7199/raspi-2024/main/images/ras004.png)

    - 라즈베리파이 연결
        - 필요한 부품
            - 라즈베리파이
            - HC-SR04 초음파 센서
            - 점퍼 케이블

    - 핀 구성 4가지
        - VCC: 전원 입력 (5V)
        - Trig: 트리거 핀, 초음파 신호를 보내는 핀
        - Echo: 에코 핀, 반사된 신호를 수신하는 핀
        - GND: 그라운드

- 라즈베리파이 입출력 키트 확인 방법
    - sudo ./build : WiringPi 라이브러리를 빌드 (관리자권한 실행)
    - (WiringPi Build script : WiringPi 라이브러리빌드를 실행) 
    - gpio -v : 설치된 WiringPi 의 버전을 확인 세부 정보 확인 가능
    - goio readall : GPIO 핀의 상태를 자세히 볼 수 있음 , 핀의 입출력 정보를 확인 할 수 있음

## 3일차
- 릴레이
    - 검출된 정보를 갖고있는 제엉 전류의 유무 또는 방향에 따라 다른 회로를 여닫는 장치
    - 입력이 어떤 값에 도달하였을 때 작동하여 다른 회로를 개폐하는 장치
    - 일종의 스위치!
    - 내부에 전자석(코일) 포함 -> 전자석은 전류가 통하게 되면 자석이 되는 성질 有
    - *전원 공급 시 릴레이 내부의 코일에 전기가 흘러 자화되고, 자화된 전자석에 의해 반대편 스위치가 작동! -> 반대편 기기에 전원 공급됨*
    - NO(Normal Open) : 열린 접점 | NC(Normal Close) : 닫힌 접점

    ![릴레이](https://raw.githubusercontent.com/som7199/raspi-2024/main/images/ras005.png)

- 스텝 모터
    - 한 바퀴의 회전을 많은 수의 스텝들로 나눌 수 있는 브러쉬리스 직류 전기 모터
    - *스텝 상태의 펄스에 순서를 부여하고, 주어진 펄스 수에 비례한 각도만큼 회전하는 모터*
    - 앙페르의 오른손 법칙 이용

    ![스텝 모터](https://raw.githubusercontent.com/som7199/raspi-2024/main/images/ras006.png)
    
    - 32개의 톱니바퀴가 4개의 전자석을 통해 한 번에 한 단계씩 회전시키는 방식으로 작동
    - 코일에 펄스 공급 시 톱니 회전
        - 펄스 순서에 따라 모터의 회전 방향 바꿀 수 있음
        - 펄스 주기(PWM)에 따라 모터의 속도 바꿀 수 있음
        - 펄스 횟수에 따라 모터의 회전 거리 바꿀 수 있음

- 가상환경 재생성
    - python -m venv --system-site-packages rpiEnv

- Flask
    ```python
    app = Flask(__name__) // Flask 클래스의 인스턴스를 만듦으로서, 플라스크 앱을 만드는 역할
    @app.route()          // 주어진 URL과 옵션들을 통해서 view 함수를 decorate
    ```
    - 플라스크에서 요청에 대한 정보는 request에 담겨있고 객체는 안전을 보장
    - 파이썬에 존재하는 requests 모듈이 아니라 플라스크 프레임워크에 존재하는 request를 불러와 사용
    - request 모듈
        - HTTP 메서드에 대한 정보를 얻을 수 있는 method
        - GET 방식으로 URL에 인자를 'key=value' 형태로 전달했을 때 그 인자를 참조할 수 있는 args
        - POST나 PUT 방식의 HTML 폼 데이터를 얻을 수 있는 form 속성
    - GET 요청 
        - 작은 양의 데이터를 보낼 때
        - 모든 파라미터를 url로 보내 요청하는 방식
        - url에 파라미터로 값을 넣는 방법은 ?를 붙이고 키=값의 쌍 형태로 넣으면 됨
        - 파라미터를 추가하고자 할 때는 &를 붙인 뒤 동일하게 추가
    - POST 요청 
        - 데이터의 양이 많을 때
        - 전달하려는 정보가 HTTP body에 포함되어 전달

## 4일차
- 4-digit 규격의 공통 음극(Common Cathode)
    - 전류가 위에서 아래로 흐름
    - 공통 단자인 COM 부분에 GND, a,b,c,d,e,f,g,dp에 VCC
        ![Common Cathod](https://raw.githubusercontent.com/som7199/raspi-2024/main/images/ras007.png)

- 4-digit 규격의 공통 양극(Common Anode)
    - 전류가 아래에서 위로 흐름
    - 공통 단자인 COM 부분에 VCC, a,b,c,d,e,f,g,dp에 GND
        ![Common Anode](https://raw.githubusercontent.com/som7199/raspi-2024/main/images/ras008.png)

- 내꺼는 공통 양극!

## 5일차
- 4 Digit FND 실습

## 6일차
- 4 Digit FND 실습
- PyQt5 로 GUI 제작

## 7일차
- PyQt5 로 GUI 제작(제출과제)