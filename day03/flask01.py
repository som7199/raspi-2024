from flask import Flask

# name 이름을 통한 Flask 객체 생성
app = Flask(__name__)

# 라우팅을 위한 뷰함수 등록
@app.route("/")
def hello():
	return "Hello Som World"

# 터미널에서 직접 실행시키면 실행파일이 main을 바뀐다
if __name__ == "__main__":
	# 실행을 위한 명령문으로 보면 된다!
	app.run(host="0.0.0.0", port="10111", debug =True)
