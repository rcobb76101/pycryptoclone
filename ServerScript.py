#!/bin/env/python

from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/', methods=['POST']
def index():
	response = make_response()
	print request.headers
	print request.data
	return response

if __name__ == '__main__':
	app.run('0.0.0.0, 8080, debug=True)