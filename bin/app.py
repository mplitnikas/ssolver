from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello interweb!!1"

@app.route("/nice/")
def nicee():
	return "Yeaaaaaah"

if __name__ == "__main__":
	app.run()