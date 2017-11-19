from flask import Flask
app = Flask(__name__)

@app.route('/')
def helloWorld():
    return 'Hello, World!'

@app.route('/logResults/')
def logResults():
	# do something with results here
	return 'LOG'

@app.route('/getTask/')
def get_HIT():
	# return task
	return 'HIT'