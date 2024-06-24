from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
	return "Flask Server Test"

@app.route("/user/<username>")
def user(username):
	return "User: %s" % username

if __name__ == "__main__":
	app.run(host="0.0.0.0", port="18080", debug=True)
