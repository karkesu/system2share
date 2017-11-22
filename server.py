from flask import Flask, render_template, request, url_for, make_response
import sys

#This allows us to specify whether we are pushing to the sandbox or live site.
DEV_ENVIROMENT_BOOLEAN = True
if DEV_ENVIROMENT_BOOLEAN:
    amazon_host = 'https://workersandbox.mturk.com/mturk/externalSubmit'
else:
    amazon_host = 'https://www.mturk.com/mturk/externalSubmit'
app = Flask(__name__)

@app.route('/')
def welcome():
    return 'Hello!'

@app.route('/getTask/<articleID>/<annotationID>', methods=['GET','POST'])
def getHIT(articleID, annotationID):

    if request.args.get('assignmentId') == 'ASSIGNMENT_ID_NOT_AVAILABLE':
        return make_response(render_template('consent.html'))

    article = getArticle(articleID)
    articleTitle = article[0]
    articleByLine = article[1]
    articleText = article[2:]

    data = {
        'amazon_host': amazon_host,
        'hitID': request.args.get('hitId'),
        'workerID': request.args.get('workerId'),
        'assignmentID': request.args.get('assignmentId'),
        'turkSubmitTo': request.args.get('turkSubmitTo'),
        'workerID': request.args.get('workerId'),
        'articleTitle': articleTitle,
        'articleByLine': articleByLine,
        'articleText': articleText,
        'annotation': annotationID
    }

    response = make_response(render_template('task.html', data = data))
    return response

def getArticle(articleID):

    f = open('static/articles/tech-hq/1.txt', 'r')
    data = f.readlines()
    f.close()
    return data
