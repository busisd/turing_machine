import flask
from turing_machine import *

app = flask.Flask(__name__)

@app.route('/')
def tm_page():
	return flask.render_template("tm_page.html")

def set_machine():
	pass

def get_states():
	pass

def main():
	app.run(host="0.0.0.0", port=2013)

if __name__ == "__main__":
	main()
