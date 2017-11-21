from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def helloWorld():
    return 'Hello, World!'

@app.route('/logResults/')
def logResults():
	# do something with results here
	return 'LOG'

@app.route('/getTask')
def getHIT():
	assignmentID = request.args.get('assignmentId')
	hitID = request.args.get('hitId')
	turkSubmitTo = request.args.get('turkSubmitTo')
	workerID = request.args.get('workerId')
	article = getArticle()
	return render_template('task.html', 
							article=article)

def getArticle():
	f = open('static/articles/test.txt', 'r')
	data = f.readlines()
	f.close()
	return data