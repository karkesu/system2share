from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def helloWorld():
    return 'Hello, World!'

@app.route('/logResults/')
def logResults():
	# do something with results here
	return 'LOG'

@app.route('/getTask/')
def getHIT():
	article = getArticle()
	return render_template('task.html', 
							article=article)


def getArticle():
	f = open('static/articles/test.txt', 'r')
	data = f.readlines()
	f.close()
	return data