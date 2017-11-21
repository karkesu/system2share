from flask import Flask, render_template, request, url_for
import sys
from create_tasks import createHIT
from setup import experimentSetup

app = Flask(__name__)

@app.route('/')
def welcome():
	createHIT()
	return 'Hello, World!'

@app.route('/logResults')
def logResults():
	# do something with results here
	return 'LOG'

@app.route('/getTask', methods=['GET','POST'])
def getHIT():
	if request.args.get('assignmentId') == "ASSIGNMENT_ID_NOT_AVAILABLE":
		pass # worker hasn't accepted task yet
	else:
		render_data = {
			"workerID": request.args.get('workerId'),
			"assignmentID": request.args.get('assignmentId'),
			"hitID": request.args.get('hitId'),
			"turkSubmitTo": request.args.get('turkSubmitTo'),
			"workerID": request.args.get('workerId'),
			"article": getArticle()
		}

		return render_template('task.html', data=render_data) # article=article)
	return

def getArticle():

	f = open('static/articles/test.txt', 'r')
	data = f.readlines()
	f.close()
	return data
