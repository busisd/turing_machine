import flask
from flask import request
from turing_machine import *
import json

app = flask.Flask(__name__)

@app.route('/')
def tm_page():
	return flask.render_template("tm_page.html")

@app.route('/generate_tm', methods=["POST"])
def set_machine():
	print("data received:", request.json)
	return json.dumps(['a','b','c'])

def main():
	app.run(host="0.0.0.0", port=2013)

if __name__ == "__main__":
	main()
