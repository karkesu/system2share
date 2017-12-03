from flask import Flask, render_template, request, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from config import *
import sys, os, random, json

# Config

# env = os.environ['APP_ENV']
env = 'dev'
app = Flask(__name__)

if env == 'dev':
    app.config.from_object('config.Dev')
    amazon_host = 'https://workersandbox.mturk.com/mturk/externalSubmit'
else:
    app.config.from_object('config.Production')
    amazon_host = 'https://www.mturk.com/mturk/externalSubmit'

db = SQLAlchemy(app)

param_names = ['task','newsfeed','newsfeed_order','promptId','prompt','placeholder','curr_cat','curr_article','curr_articleTitle','curr_articleByLine','curr_articleText','assignmentId','hitId','workerId','amazon_newsfeed_order','amazon_newsfeed_annotation_a1','amazon_newsfeed_annotation_a2','amazon_articleId','amazon_time_reading','amazon_time_writing','amazon_annotation','apple_newsfeed_annotation_a1','apple_newsfeed_annotation_a2','apple_articleId','apple_time_reading','apple_time_writing','apple_annotation','uber_newsfeed_annotation_a1','uber_newsfeed_annotation_a2','uber_articleId','uber_time_reading','uber_time_writing','uber_annotation']

poss_assignments = {
    'newsfeed_order': ['1,2','2,1'],
    'promptId': ['0','1','2','3']
}
    # 'task'
    # 'newsfeed'
    # 'newsfeed_order'
    # 'promptId'
    # 'prompt'
    # 'placeholder'
    # 'curr_cat'
    # 'curr_article'
    # 'curr_articleTitle'
    # 'curr_articleByLine'
    # 'curr_articleText'
    # 'assignmentId'
    # 'hitId'
    # 'workerId'
    # 'amazon_newsfeed_annotation_a1'
    # 'amazon_newsfeed_annotation_a2'
    # 'amazon_articleId'
    # 'amazon_time_reading'
    # 'amazon_time_writing'
    # 'amazon_annotation'
    # 'apple_newsfeed_annotation_a1'
    # 'apple_newsfeed_annotation_a2'
    # 'apple_articleId'
    # 'apple_time_reading'
    # 'apple_time_writing'
    # 'apple_annotation'
    # 'uber_newsfeed_annotation_a1'
    # 'uber_newsfeed_annotation_a2'
    # 'uber_articleId'
    # 'uber_time_reading'
    # 'uber_time_writing'
    # 'uber_annotation'


# Database Models

class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    newsfeed = db.Column(db.String(1), nullable=False)
    newsfeed_order = db.Column(db.String(20), nullable=True)
    promptId = db.Column(db.String(1), nullable=False)
    # assignmentId = db.Column(db.String(50), nullable=False)
    # hitId = db.Column(db.String(50), nullable=False)
    # workerId = db.Column(db.String(50), nullable=False)
    # amazon_newsfeed_order = db.Column(db.String(20), nullable=True)
    # amazon_newsfeed_annotation_a1annotation = db.Column(db.String(1), nullable=True)
    # amazon_newsfeed_annotation_a2annotation = db.Column(db.String(1), nullable=True)
    # amazon_articleId = db.Column(db.String(1), nullable=False)
    # amazon_promptId = db.Column(db.String(1), nullable=False)
    # amazon_time_reading = db.Column(db.String(20), nullable=False)
    # amazon_time_writing = db.Column(db.String(20), nullable=False)
    # amazon_annotation = db.Column(db.String(1000), nullable=True)
    # apple_newsfeed_order = db.Column(db.String(20), nullable=True)
    # apple_newsfeed_annotation_a1annotation = db.Column(db.String(1), nullable=True)
    # apple_newsfeed_annotation_a2annotation = db.Column(db.String(1), nullable=True)
    # apple_articleId = db.Column(db.String(1), nullable=False)
    # apple_promptId = db.Column(db.String(1), nullable=False)
    # apple_time_reading = db.Column(db.String(20), nullable=False)
    # apple_time_writing = db.Column(db.String(20), nullable=False)
    # apple_annotation = db.Column(db.String(1000), nullable=True)
    # uber_newsfeed_order = db.Column(db.String(20), nullable=True)
    # uber_newsfeed_annotation_a1annotation = db.Column(db.String(1), nullable=True)
    # uber_newsfeed_annotation_a2annotation = db.Column(db.String(1), nullable=True)
    # uber_articleId = db.Column(db.String(1), nullable=False)
    # uber_promptId = db.Column(db.String(1), nullable=False)
    # uber_time_reading = db.Column(db.String(20), nullable=False)
    # uber_time_writing = db.Column(db.String(20), nullable=False)
    # uber_annotation = db.Column(db.String(1000), nullable=True)

# Views

@app.route('/submit')
def submit():
    # create test entry
    exp = Experiment()
    # get dictionary of params and values from URL
    params = getParams()
    # delete unnecessary params from larger list
    db_params = param_names
    for p in ['task','prompt','placeholder','curr_cat','curr_article','curr_articleTitle','curr_articleByLine','curr_articleText']:
        if p in db_params:
            db_params.remove(p)
    # assign values to Experiment params
    for p in db_params:
        setattr(exp, p, params[p])
        print(params[p])
    # assign repetitive values
    for company in ['amazon','apple','uber']:
        setattr(exp,(company+'_newsfeed_order'),params['newsfeed_order'])
        setattr(exp,(company+'_promptId'),params['promptId'])
    # db.session.add(exp)
    # db.session.commit()
    
    print(exp)
    exp2 = Experiment.query.filter_by(newsfeed='3').all()
    print(exp2)
    return 'submitted'
    # db.session.commit()
    # exp = Experiment.query.filter_by(exp=1, context=0).first()
    # if exp == None:
    #     exp=Experiment(exp=1, context=0, iterations=0)
    #     db.session.add(exp)
    # exp.iterations = exp.iterations + 1
    # db.session.commit()
    # return str(exp.iterations)

@app.route('/test/')
def test():
    targetLink = request.url_root 
    targetLink += 'getTask/' #+ articleCategory + '/' + articleID
    targetLink += '?' + request.query_string.decode('utf-8')
    response = make_response(render_template('test.html', targetLink=targetLink))
    return response

@app.route('/getTask/', methods=['GET','POST'])
def getHIT():

    # Before HIT is picked up, show consent form
    if request.args.get('assignmentId') == 'ASSIGNMENT_Id_NOT_AVAILABLE':
        return make_response(render_template('consent.html'))

    # Get params from URLs
    params = getParams()

    # ALL PARAMS
    # 'task'
    # 'newsfeed'
    # 'newsfeed_order'
    # 'promptId'
    # 'prompt'
    # 'placeholder'
    # 'curr_cat'
    # 'curr_article'
    # 'curr_articleTitle'
    # 'curr_articleByLine'
    # 'curr_articleText'
    # 'assignmentId'
    # 'hitId'
    # 'workerId'
    # 'amazon_newsfeed_annotation_a1'
    # 'amazon_newsfeed_annotation_a2'
    # 'amazon_articleId'
    # 'amazon_time_reading'
    # 'amazon_time_writing'
    # 'amazon_annotation'
    # 'apple_newsfeed_annotation_a1'
    # 'apple_newsfeed_annotation_a2'
    # 'apple_articleId'
    # 'apple_time_reading'
    # 'apple_time_writing'
    # 'apple_annotation'
    # 'uber_newsfeed_annotation_a1'
    # 'uber_newsfeed_annotation_a2'
    # 'uber_articleId'
    # 'uber_time_reading'
    # 'uber_time_writing'
    # 'uber_annotation'

    # STILL UNASSIGNED
    ## 'assignmentId'
    ## 'hitId'
    ## 'workerId'
    ## 'task'
    # 'newsfeed'
    ## 'newsfeed_order'
    ## 'promptId'
    ## 'prompt'
    ## 'placeholder'
    ## 'curr_cat'
    ## 'curr_article'
    ## 'curr_articleTitle'
    ## 'curr_articleByLine'
    ## 'curr_articleText'
    # 'amazon_newsfeed_annotation_a1'
    # 'amazon_newsfeed_annotation_a2'
    # 'amazon_articleId'
    # 'amazon_time_reading'
    # 'amazon_time_writing'
    # 'amazon_annotation'
    # 'apple_newsfeed_annotation_a1'
    # 'apple_newsfeed_annotation_a2'
    # 'apple_articleId'
    # 'apple_time_reading'
    # 'apple_time_writing'
    # 'apple_annotation'
    # 'uber_newsfeed_annotation_a1'
    # 'uber_newsfeed_annotation_a2'
    # 'uber_articleId'
    # 'uber_time_reading'
    # 'uber_time_writing'
    # 'uber_annotation'

    ###########################################################
    # The following parameters stay constant for all categories
    ###########################################################
    # show newsfeed?
    if params['newsfeed'] is None:
        # TO UPDATE
        params['newsfeed'] = '1' #showNewsFeed()

    # what order will the newsfeed articles be shown?
    if params['newsfeed'] == '1' and params['newsfeed_order'] is None:
        params['newsfeed_order'] = getLeastFrequent('newsfeed_order', poss_assignments['newsfeed_order'],groupBy=None)

    # assign promptId, prompt, placeholder
    if params['promptId'] is None:
        params['promptId'] = getLeastFrequent('promptId',poss_assignments['promptId'],groupBy=None)
        with open('static/articles/annotations.json') as json_file:
            d = "["+ str(json_file.read())+"]"
            prompts = json.loads(d)
            prompt = prompts[int(params['promptId'])]
            params['prompt'] = prompt['prompt']
            params['placeholder'] = prompt['placeholder']

    ###########################################################
    # Dynamic variables! Updated throughout experiment
    ###########################################################
    # task: 0 = newsfeed, 1 = reading/annotating, 2 = reviewing
    params['task'] = getNextTask(params['task'])

    # current category 
    'curr_cat'
    # 'curr_article'
    'curr_article'
    # 'curr_articleTitle'
    'curr_articleTitle'
    # 'curr_articleByLine'
    'curr_articleByLine'
    # 'curr_articleText'
    'curr_articleText'
    # assign empty params
    for p in ['']:
        pass


    # Get prompts
    
    

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

    

    #experiment.query.getall
    # do not show newsfeed if difference between #annotations/articles > 5

    data = params
    data['amazon_host'] = amazon_host
    # for d in data:
    #     print(str(d)+" ======= "+str(data[d]))

    targetLink = request.url_root 
    targetLink += 'getTask/' #+ articleCategory + '/' + articleID
    
    if data['newsfeed']=='1' and data['task']=='0':
        response = make_response(render_template('newsfeed.html', data = data))
    else:
        response = make_response(render_template('task.html', data = data))
    targetLink += '?' + request.query_string.decode('utf-8')
    response = make_response(render_template('test.html', targetLink=targetLink))
    return response

def getArticle(articleCategory, articleId):

    f = open('static/articles/' + articleCategory + '/' + articleId + '.txt', 'r', encoding='utf-8')
    data = f.readlines()
    f.close()
    return data

def getLeastFrequent(param,options,groupBy):
    leastFrequent = options[0]
    leastFrequentCount = 0
    for option in options:
        args = {param:option}
        count = len(Experiment.query.filter_by(**args).all())
        print(param+" = "+option+" === "+str(count))
        if count <= leastFrequentCount:
            leastFrequent = option
            leastFrequentCount = count
    print("LEAST FREQUENT ="+leastFrequent)
    return leastFrequent

def getNextTask(task):
    next_task = 1 if task == None else Integer(task) + 1
    print("NEXT TASK!!!!!")
    print(next_task)
    return str(next_task)

def showNewsFeed(category):
    # if total submissions < 1 per article return false
    # if max difference b/w articles > 5 return false
    Experiment.query.filter_by(curr_cat='3').all()
    return str(0)

def getPromptId():
    return str(0)

def getParams():
    params = {}
    for p in param_names:
        key = p
        val = request.args.get(p) if request.args.get(p) else None

        if key == 'newsfeed_order' and val is not None: #special cases for arrays
            array = val.split(",")
            params[key] = array
        else:
            params[key] = val
    return params
