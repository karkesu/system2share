from flask import Flask, render_template, request, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from config import *
import sys, os, random

# Config

env = os.environ['APP_ENV']
app = Flask(__name__)

if env == 'dev':
    app.config.from_object('config.Dev')
    amazon_host = 'https://workersandbox.mturk.com/mturk/externalSubmit'
else:
    app.config.from_object('config.Production')
    amazon_host = 'https://www.mturk.com/mturk/externalSubmit'

db = SQLAlchemy(app)

# Database Models

class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exp = db.Column(db.Integer, nullable=False)
    context = db.Column(db.Integer, nullable=False)
    iterations = db.Column(db.Integer, nullable=False)

# Views

# this route is a way to test the database. Just reloading should increment this
@app.route('/')
def welcome():
    exp = Experiment.query.filter_by(exp=1, context=0).first()
    if exp == None:
        exp=Experiment(exp=1, context=0, iterations=0)
        db.session.add(exp)
    exp.iterations = exp.iterations + 1
    db.session.commit()
    return str(exp.iterations)

@app.route('/getTask/<articleCategory>/<articleID>', methods=['GET','POST'])
def getHIT(articleID, articleCategory):

    if request.args.get('assignmentId') == 'ASSIGNMENT_ID_NOT_AVAILABLE':
        return make_response(render_template('consent.html'))

    article = getArticle(articleCategory, articleID)
    articleTitle = article[0]
    articleByLine = article[1]
    articleText = article[2:]

    prompts = [
        {"prompt": "",
            "placeholder": "Say something about this..."},
        {"prompt": "Share a quote to give people more context.",
            "placeholder": ""},
        {"prompt": "Summarize the article.",
            "placeholder": ""},
        {"prompt": "How does this issue affect you or someone you know?",
            "placeholder": "Sharing a personal story helps others understand the real impacts of this issue."},
        {"prompt": "Argue for or against the main viewpoints of this article. Is there anything missing that you would like to learn more about?",
            "placeholder": "Do you have any specific questions?"},
        {"prompt": "What should we do about this issue? Who should care and why?",
            "placeholder": ""}
    ]

    promptID = random.randint(0,5)
    data = {
        'amazon_host': amazon_host,
        'hitID': request.args.get('hitId'),
        'workerID': request.args.get('workerId'),
        'assignmentID': request.args.get('assignmentId'),
        'turkSubmitTo': request.args.get('turkSubmitTo'),
        'workerID': request.args.get('workerId'),
        'articleCategory': articleCategory,
        'articleID': articleID,
        'articleTitle': articleTitle,
        'articleByLine': articleByLine,
        'articleText': articleText,
        'promptID': promptID,
        'prompts': prompts
    }

    response = make_response(render_template('task.html', data = data))
    return response

def getArticle(articleCategory, articleID):

    f = open('static/articles/' + articleCategory + '/' + articleID + '.txt', 'r', encoding='utf-8')
    data = f.readlines()
    f.close()
    return data
