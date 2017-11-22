from flask import Flask, render_template, request, url_for, make_response
import sys
import random

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

@app.route('/getTask/<articleCategory>/<articleID>', methods=['GET','POST'])
def getHIT(articleID, articleCategory):

    if request.args.get('assignmentId') == 'ASSIGNMENT_ID_NOT_AVAILABLE':
        return make_response(render_template('consent.html'))

    article = getArticle(articleCategory, articleID)
    articleTitle = article[0]
    articleByLine = article[1]
    articleText = article[2:]

    annotations = {
        "0":"Say something about this...",
        "1": "What's your opinion on this issue?",
        "2": "How does this issue affect you or someone you know? Sharing a personal story helps others understand the real impacts of this issue.",
        "3": "How could others help you understand this issue better? Do you have any specific questions?",
        "4": "What should we do about this issue? Who should care and why?"
        }

    annotationID = str(random.randint(0,4))    

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
        'annotationID': annotationID,
        'annotation': annotations[annotationID]
    }

    response = make_response(render_template('task.html', data = data))
    return response

def getArticle(articleCategory, articleID):

    f = open('static/articles/' + articleCategory + '/' + articleID + '.txt', 'r')
    data = f.readlines()
    f.close()
    return data
