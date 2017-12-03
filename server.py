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
    context = db.Column(db.Integer, nullable=False) # article/promptId
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

@app.route('/getTask/', methods=['GET','POST']) #@app.route('/getTask/<articleCategory>/<articleId>', methods=['GET','POST'])
def getHIT():

    if request.args.get('assignmentId') == 'ASSIGNMENT_Id_NOT_AVAILABLE':
        return make_response(render_template('consent.html'))

    param_names = ['task','newsfeed','newsfeed_order','promptId','prompt','placeholder','curr_cat','curr_article','curr_articleTitle','curr_articleByLine','curr_articleText','assignmentId','hitId','workerId','amazon_newsfeed_order','amazon_newsfeed_annotation_a1','amazon_newsfeed_annotation_a2','amazon_articleId','amazon_promptId','amazon_time_reading','amazon_time_writing','amazon_annotation']
    # SAME ACROSS ALL CATEGORIES/META params:
    # newsfeed      : 2 variations: 0,1                 DISTRIBUTION = ???; dependent on distribution of articles annotated
    # newsfeed_order: 2 variations: 1,2 or 2,1""        P(i) = 1/2; x3 vars, one for each cat
    # promptId      : 4 variations: 0,1,2,3             P(i) = 1/4
    # curr_cat      : 3 variations: amazon, apple, uber (always in same order)
    # curr_article  : 2 variations: 1, 2
    # assignmentId
    # hitId
    # workerId

    # PER CATEGORY:
    # amazon_newsfeed_order             : 1,2 or 2,1""  (same across all categories)
    # amazon_newsfeed_annotation_a1     : 0,1,2,3,""    (rand; dependent on newsfeed annotation distribution)
    # amazon_newsfeed_annotation_a2     : 0,1,2,3,""    (rand; dependent on newsfeed annotation distribution)
    # amazon_articleId                  : 1,2           (automatically assigned if no newsfeed)
    # amazon_promptId                   : 0,1,2,3       (same across all categories)
    # amazon_time_reading               :
    # amazon_time_writing               : 
    # amazon_annotation                 :                

    # apple_newsfeed_order             : 1,2 or 2,1""  (same across all categories)
    # apple_newsfeed_annotation_a1     : 0,1,2,3,""    (rand; dependent on newsfeed annotation distribution)
    # apple_newsfeed_annotation_a2     : 0,1,2,3,""    (rand; dependent on newsfeed annotation distribution)
    # apple_articleId                  : 1,2           (automatically assigned if no newsfeed)
    # apple_promptId                   : 0,1,2,3       (same across all categories)
    # apple_time_reading               :
    # apple_time_writing               : 
    # apple_annotation                 :     

    # uber_newsfeed_order             : 1,2 or 2,1""  (same across all categories)
    # uber_newsfeed_annotation_a1     : 0,1,2,3,""    (rand; dependent on newsfeed annotation distribution)
    # uber_newsfeed_annotation_a2     : 0,1,2,3,""    (rand; dependent on newsfeed annotation distribution)
    # uber_articleId                  : 1,2           (automatically assigned if no newsfeed)
    # uber_promptId                   : 0,1,2,3       (same across all categories)
    # uber_time_reading               :
    # uber_time_writing               : 
    # uber_annotation                 :                
    
    params = {}
    for p in param_names:
        key = p
        val = request.args.get(p) if request.args.get(p) else ''
        if key == 'newsfeed_order': #special cases for arrays
            array = val.split(",")
            params[key] = array
        else:
            params[key] = val

    # for p in params:
    #     print(str(p)+" ===================== "+params[p])
    
    # Get newsfeed
    if params['newsfeed']=='1' and params['task']=='0':
        cat = params['curr_cat'] if params['curr_cat'] else ''
        summaries_dict = {}
        for articleId in params['newsfeed_order']:
            article = getArticle(cat, articleId)
            content = str(article[2:])
            summaries_dict[articleId] = {}
            summaries_dict[articleId]['title'] = article[0]
            summaries_dict[articleId]['byLine'] = article[1]
            summaries_dict[articleId]['preview'] = content[:150]+"..."
            summaries_dict[articleId]['annotation'] = 'ANNOTATION'
        print(summaries_dict)
        params['summaries'] = summaries_dict

    # Get articles
    if params['curr_cat'] and params['curr_article']:
        article = getArticle(params['curr_cat'], params['curr_article'])
        params['curr_articleTitle'] = article[0]
        params['curr_articleByLine'] = article[1]
        params['curr_articleText'] = article[2:]

    # Get prompts
    with open('static/articles/annotations.json') as json_file:
        d = "["+ str(json_file.read())+"]"
        prompts = json.loads(d)
    # prompts = json_data
    prompt = prompts[int(params['promptId'])]
    params['prompt'] = prompt['prompt']
    params['placeholder'] = prompt['placeholder']

    
    # data = {
    #     'amazon_host': amazon_host,
    #     'hitId': request.args.get('hitId'),
    #     'workerId': request.args.get('workerId'),
    #     'assignmentId': request.args.get('assignmentId'),
    #     'turkSubmitTo': request.args.get('turkSubmitTo'),
    #     'workerId': request.args.get('workerId'),
    #     'articleCategory': params['curr_cat'],
    #     'articleId': params['curr_article'],
    #     'articleTitle': articleTitle,
    #     'articleByLine': articleByLine,
    #     'articleText': articleText,
    #     'promptId': promptId,
    #     'prompts': prompts
    # }
    data = params
    data['amazon_host'] = amazon_host
    for d in data:
        print(str(d)+" ======= "+str(data[d]))
    if data['newsfeed']=='1' and data['task']=='0':
        response = make_response(render_template('newsfeed.html', data = data))
    else:
        response = make_response(render_template('task.html', data = data))
    return response

def getArticle(articleCategory, articleId):

    f = open('static/articles/' + articleCategory + '/' + articleId + '.txt', 'r', encoding='utf-8')
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
