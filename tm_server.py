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
	TM = create_tm_from(request.json["tm_data"], start_state=request.json["start_state"])
	if type(TM) == list:
		print(TM)
		return json.dumps({"error": True, "data": TM})
	else:
		errors = TM.start_sim(request.json["input_string"])
		if errors:
			return(json.dumps({"error": True, "data": errors}))
		steps = get_steps(TM, 100)
		return json.dumps(steps)

def main():
	app.run(host="0.0.0.0", port=2013)

if __name__ == "__main__":
	main()
