from flask import Flask, render_template, request, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from config import *
import sys, os, random, json

# Config

env = 'dev' #os.environ['APP_ENV']
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
    exp = db.Column(db.Integer, nullable=False) # 1 or 2 for annotating/viewing
    context = db.Column(db.Integer, nullable=False) # article/promptID
    iterations = db.Column(db.Integer, nullable=False) # 

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

    print("REQUEST ARGS")
    print(request.args.get('articleID'))
    # Get articles
    article = getArticle(articleCategory, articleID)
    articleTitle = article[0]
    articleByLine = article[1]
    articleText = article[2:]

    # Get annotations

    # Get prompts
    with open('static/articles/annotations.json') as json_file:
        d = "["+ str(json_file.read())+"]"
        json_data = json.loads(d)
    prompts = json_data
    promptID = random.randint(0,5)

    # articleIDs = [[2,3,1],[3,1,2],[1,3,2]]
    # articleCats = ['tech-hq','sharing-econ','mooc']
    # 
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
    for d in data:
        print(type(d))

    response = make_response(render_template('task.html', data = data))
    return response

def getArticle(articleCategory, articleID):

    f = open('static/articles/' + articleCategory + '/' + articleID + '.txt', 'r', encoding='utf-8')
    data = f.readlines()
    f.close()
    return data

def load_json_multiple(segment):
    chunk = ""
    for segment in segments:
        chunk += segment
        try:
            yield json.loads(chunk)
            chunk = ""
        except ValueError:
            pass
