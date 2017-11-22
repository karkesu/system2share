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

    annotations = [
        #0
        {"annotation": "",
        "placeholder": "Say something about this..."},
        #1
        {"annotation": "Which quote would you share to give people more context?",
        "placeholder": ""},
        #2
        {"annotation": "What's your opinion on this issue?",
        "placeholder": ""},
        #3
        {"annotation": "How does this issue affect you or someone you know?",
        "placeholder": "Sharing a personal story helps others understand the real impacts of this issue."},
        #4
        {"annotation": "How could others help you understand this issue better?",
        "placeholder": "Do you have any specific questions?"},
        #5
        {"annotation": "What should we do about this issue? Who should care and why?",
        "placeholder": ""},
        ]


    annotationID = random.randint(0,5)

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
        'annotation': annotations[annotationID]["annotation"],
        'placeholder': annotations[annotationID]["placeholder"]
    }

    response = make_response(render_template('task.html', data = data))
    return response

def getArticle(articleCategory, articleID):

    f = open('static/articles/' + articleCategory + '/' + articleID + '.txt', 'r', encoding='utf-8')
    data = f.readlines()
    f.close()
    return data
