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

# This is basically a superset of all the variables we'd want to save. params checks against this list to save URL args. Easier to read (vertical) version below in the db Model
param_names = ['assignmentId','hitId','workerId','task','newsfeed','newsfeed_order','promptId','prompt','placeholder','curr_cat','curr_article','curr_articleTitle','curr_articleByLine','curr_articleText','amazon_newsfeed_annotation_a1','amazon_newsfeed_annotation_a2','amazon_annotation_content_a1','amazon_annotation_content_a2','amazon_articleId','amazon_promptId','amazon_time_reading','amazon_time_writing','amazon_annotation','amazon_likert_summary_evaluation','amazon_likert_prior_knowledge','amazon_likert_learning','apple_newsfeed_annotation_a1','apple_newsfeed_annotation_a2','apple_annotation_content_a1','apple_annotation_content_a2','apple_articleId','apple_promptId','apple_time_reading','apple_time_writing','apple_annotation','apple_likert_summary_evaluation','apple_likert_prior_knowledge','apple_likert_learning','uber_newsfeed_annotation_a1','uber_newsfeed_annotation_a2','uber_annotation_content_a1','uber_annotation_content_a2','uber_articleId','uber_promptId','uber_time_reading','uber_time_writing','uber_annotation','uber_likert_summary_evaluation','uber_likert_prior_knowledge','uber_likert_learning']

# For cleanup. So we don't have to pass around all the params everywhere. Was going to do one big data dump at the end
redundant_params = ['prompt','placeholder','newsfeed','curr_articleTitle','curr_articleByLine','curr_articleText']
# Mostly used for populating variants
poss_assignments = {
    'newsfeed_order': ['12','21'],
    'promptId': ['0','1','2','3'],
    'curr_cat': ['amazon','apple','uber'],
    'curr_article': ['1','2'],
}



# Database Models

class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    newsfeed = db.Column(db.Boolean, nullable=False)
    newsfeed_order = db.Column(db.String(2), nullable=True)
    promptId = db.Column(db.Integer, nullable=False)
    # assignmentId = db.Column(db.String(50), nullable=False)
    # hitId = db.Column(db.String(50), nullable=False)
    # workerId = db.Column(db.String(50), nullable=False)
    amazon_newsfeed_order = db.Column(db.String(10), nullable=True)
    amazon_newsfeed_annotation_a1 = db.Column(db.Integer, nullable=True)
    amazon_newsfeed_annotation_a2 = db.Column(db.Integer, nullable=True)
    amazon_articleId = db.Column(db.Integer, nullable=True)
    # amazon_promptId = db.Column(db.Integer, nullable=False)
    # amazon_time_reading = db.Column(db.String(20), nullable=False)
    # amazon_time_writing = db.Column(db.String(20), nullable=False)
    amazon_annotation = db.Column(db.String(1000), nullable=True)
    ## apple_newsfeed_order = db.Column(db.String(20), nullable=True)
    ## apple_newsfeed_annotation_a1annotation = db.Column(db.String(1), nullable=True)
    ## apple_newsfeed_annotation_a2annotation = db.Column(db.String(1), nullable=True)
    apple_articleId = db.Column(db.Integer, nullable=False)
    ## apple_promptId = db.Column(db.Integer, nullable=False)
    ## apple_time_reading = db.Column(db.String(20), nullable=False)
    ## apple_time_writing = db.Column(db.String(20), nullable=False)
    ## apple_annotation = db.Column(db.String(1000), nullable=True)
    ## uber_newsfeed_order = db.Column(db.String(20), nullable=True)
    ## uber_newsfeed_annotation_a1annotation = db.Column(db.String(1), nullable=True)
    ## uber_newsfeed_annotation_a2annotation = db.Column(db.String(1), nullable=True)
    ## uber_articleId = db.Column(db.Integer, nullable=False)
    ## uber_promptId = db.Column(db.Integer, nullable=False)
    ## uber_time_reading = db.Column(db.String(20), nullable=False)
    ## uber_time_writing = db.Column(db.String(20), nullable=False)
    ## uber_annotation = db.Column(db.String(1000), nullable=True)

# Views

@app.route('/submit')
def submit():                                   # can submit here at the end? or along the way.
    exp = Experiment()                          # create test entry
    params = getParamsFromURL(request.args)     # get dictionary of params and values from URL
    db_params = param_names                     
    for p in redundant_params:                  # delete unnecessary params from larger list
        if p in db_params:
            db_params.remove(p)
    for p in db_params:                         # assign values to Experiment params
        setattr(exp, p, params[p])
        print(params[p])
    for company in ['amazon','apple','uber']:   # assign repetitive values
        setattr(exp,(company+'_newsfeed_order'),params['newsfeed_order'])
        setattr(exp,(company+'_promptId'),params['promptId'])
    # db.session.add(exp)
    # db.session.commit()
    
    print(exp)
    exp2 = Experiment.query.filter_by(newsfeed='3').all()
    print(exp2)
    return 'submitted'

@app.route('/test/')
def test():
    targetLink = request.url_root 
    targetLink += 'getTask/' #+ articleCategory + '/' + articleID
    targetLink += '?' + request.query_string.decode('utf-8')
    response = make_response(render_template('test.html', targetLink=targetLink))
    return response

@app.route('/getTask/', methods=['GET','POST'])
def getHIT():
    targetLink = request.url_root

    # Before HIT is picked up, show consent form
    if request.args.get('assignmentId') == 'ASSIGNMENT_Id_NOT_AVAILABLE':
        return make_response(render_template('consent.html'))

    

    # ALL PARAMS
    # 'assignmentId'
    # 'hitId'
    # 'workerId'
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
    # 'amazon_newsfeed_annotation_a1'
    # 'amazon_newsfeed_annotation_a2'
    # 'amazon_articleId'
    # 'amazon_promptId'
    # 'amazon_time_reading'
    # 'amazon_time_writing'
    # 'amazon_annotation'
    # 'apple_newsfeed_annotation_a1'
    # 'apple_newsfeed_annotation_a2'
    # 'apple_articleId'
    # 'apple_promptId'
    # 'apple_time_reading'
    # 'apple_time_writing'
    # 'apple_annotation'
    # 'uber_newsfeed_annotation_a1'
    # 'uber_newsfeed_annotation_a2'
    # 'uber_articleId'
    # 'uber_promptId'
    # 'uber_time_reading'
    # 'uber_time_writing'
    # 'uber_annotation'


    # Get/reset params from URLs
    params = getParamsFromURL(request.args)

    ###########################################################
    # INITIALIZE BLANK STATE
    # task: 0 = newsfeed, 1 = reading/annotating, 2 = reviewing
    params['task'] = 0 if params['task'] is None else params['task']
    params['curr_cat'] = 'amazon' if params['curr_cat'] is None else params['curr_cat']


    ###########################################################
    # FOR EACH ROUND
    ###########################################################
    # we're in the newsfeed view
    if params['task'] == 0:
        params['newsfeed'] = showNewsfeed(params['curr_cat']) 
    # TESTING: set this to true to see the newsfeed
    # params['newsfeed'] = True

    ###########################################################
    # The following parameters stay constant for all categories
    ###########################################################
    # what order will the newsfeed articles be shown? Set this once for the entire experiment.
    if params['newsfeed'] == True and params['newsfeed_order'] is None:
        params['newsfeed_order'] = getLeastFrequent('newsfeed_order', poss_assignments['newsfeed_order'],None)
    # assign promptId, prompt, placeholder
    if params['promptId'] is None:
        params['promptId'] = getLeastFrequent('promptId',poss_assignments['promptId'],None)

    # checkParams
    
    ###########################################################
    # Task 0: Newsfeed
    if params['task'] == 0:
        # Show newsfeed? Or direct straight to article? Currently varies per category. Could standardize.
        if params['newsfeed'] == True:
            # Set annotations for each article; returns a dictionary
            summaries_dict = setNewsfeedContent(params)
            data = {'summaries':summaries_dict, 'curr_cat': params['curr_cat']}
        else: 
            # Set article content and prompt; returns a dictionary
            article_dict = setArticleContent(params)
            data = article_dict
            curr_articleId_param = params['curr_cat']+"_articleId"
            params[curr_articleId_param] = params['curr_article']
            # print(params[curr_articleId_param])
            # print(curr_articleId_param)

        # preparing to move on to next step
        if params['newsfeed'] == True:
            targetLink = getNextLink(targetLink,params)
            # checkParams(params)
            # print(targetLink)
            return make_response(render_template('newsfeed.html', data=data, targetLink=targetLink))
        else:
            targetLink = getNextLink(targetLink,params) # print(targetLink)
            return make_response(render_template('task.html', data=data, targetLink=targetLink))


    ###########################################################
    # Task 1: Annotate article
    # populate the article. curr_article should have been passed.
    if params['task'] == 1 and params['curr_article'] and params['curr_cat']:
        # print("########################################################### task 1 triggered")
        # checkParams(params)
        article_dict = setArticleContent(params)
        data = article_dict
        curr_articleId_param = params['curr_cat']+"_articleId"
        params[curr_articleId_param] = params['curr_article']
        
        targetLink = getNextLink(targetLink,params)
        return make_response(render_template('task.html', data=data, targetLink=targetLink))

    

    ###########################################################
    # Task 2: Review article/summaries
    task2_prereq = ['newsfeed','newsfeed_order','promptId','curr_cat','curr_article'] #'annotation_content'

    if params['task'] == 2 and checkPrereq(task2_prereq,params):
        data = {}
        for p in task2_prereq:
            data[p] = params[p]
        annotation_id = params['curr_cat']+"_annotation_content_a"+params['curr_article']
        if params[annotation_id]:
            data[annotation_id]=params[annotation_id]

        targetLink = getNextLink(targetLink,params)
        return make_response(render_template('review.html', data=data, targetLink=targetLink))



    #################################################
    checkParams(params)

    data = params
    data['amazon_host'] = amazon_host

    # all placeholders
    targetLink = getNextLink(targetLink,params)
    response = make_response(render_template('test.html', targetLink=targetLink))
    return response

def getArticle(articleCategory, articleId):
    # open one article
    f = open('static/articles/' + articleCategory + '/' + articleId + '.txt', 'r', encoding='utf-8')
    data = f.readlines()
    f.close()
    return data

def getLeastFrequent(param,options,additional_info):
    # for counterbalancing our experiements
    # e.g. param = 'promptId', options = ['0','1','2','3'],additional_info=None)
    # e.g. param = 'newsfeed_order', options = ['1,2','2,1'],additional_info=None)
    # e.g. param = 'amazon_articleId', options = ['0','1'],additional_info={'promptId':3})
    leastFrequent = options[0]
    leastFrequentCount = 0
    for option in options:
        args = {param:option}
        if additional_info:
            for a in additional_info:
                args[a] = additional_info[a]
        count = Experiment.query.filter_by(**args).count()
        if count <= leastFrequentCount:
            leastFrequent = option
            leastFrequentCount = count
    # print("LEAST FREQUENT ="+leastFrequent)
    return leastFrequent

def getRandomAnnotation(param,value,resultField):
    # return actual annotation if there is one; otherwise ''
    args = {param:value}
    all_annotations = Experiment.query.filter_by(**args).all()
    if len(all_annotations) == 0:
        return None
    else:
        rand = random.randint(0,len(all_annotations) - 1)
        return all_annotations[rand] #[resultField]

def getNextTask(task):
    # Initiate at 0 or cycle through to next phase
    if task == 2 or task is None:
        next_task = 0
    else:
        next_task = task + 1
    return next_task

# This can currently change per article. Feel free to standardize
def showNewsfeed(category):
    # if total submissions < 1 per article return false
    # if max difference b/w articles > 5 return false
    counts = []
    for option in [1,2]:
        temp_param = category+'_articleId'
        args = {temp_param: str(option)}
        count = len(Experiment.query.filter_by(**args).all())
        # if total submissions < 1 per article return false
        if count < 1:
            return False
        counts.append(count)
    # if max difference b/w articles > 5 return false
    return False if abs(counts[0]-counts[1])>5 else True

# This is probably a bit opaque..Basically generating and populating summaries & annotations from other users
def setNewsfeedContent(params):
    annotation1 = params['curr_cat']+"_newsfeed_annotation_a1"
    annotation2 = params['curr_cat']+"_newsfeed_annotation_a2"
    for annotation in [annotation1, annotation2]:
        num = annotation[-1]
        annotationId = getLeastFrequent(annotation,poss_assignments['promptId'],{'newsfeed_order':params['newsfeed_order']})
        annotation_field = params['curr_cat']+"_annotation"
        annotation_rand = params['curr_cat']+"_annotation_content_a"+num
        annotation_content = getRandomAnnotation(annotation,annotationId,annotation_field)
        params[annotation_rand] = str(annotation_content.__dict__[annotation_field]) if annotation_content else ""
        params[annotation] = annotationId

    # Get newsfeed summaries content
    summaries_dict = {}
    for articleId in [params['newsfeed_order'][0],params['newsfeed_order'][1]]:
        annotation_rand = params['curr_cat']+"_annotation_content_a"+articleId
        article = getArticle(params['curr_cat'], articleId)
        summaries_dict[articleId] = {}
        summaries_dict[articleId]['title'] = article[0]
        summaries_dict[articleId]['byLine'] = article[1]
        summaries_dict[articleId]['preview'] = article[2:3][0][:150]+"..."
        summaries_dict[articleId]['annotation'] = params[annotation_rand]

    return summaries_dict

# setting stuff up for annotating a single article
def setArticleContent(params):
    curr_topic = params['curr_cat']+"_articleId" # e.g. 'amazon_articleId'
    article_dict = {}
    if params['curr_article'] is None:
        params['curr_article'] = getLeastFrequent(curr_topic,poss_assignments['curr_article'], None)
    # what article is the user annotating?
    if params['curr_cat'] and params['curr_article']:
        article = getArticle(params['curr_cat'], params['curr_article'])
        article_dict['curr_articleTitle'] = article[0]
        article_dict['curr_articleByLine'] = article[1]
        article_dict['curr_articleText'] = article[2:]
        article_dict['curr_cat'] = params['curr_cat']

    # assign promptId, prompt, placeholder
    if params['promptId']:
        with open('static/articles/annotations.json') as json_file:
            d = "["+ str(json_file.read())+"]"
            prompts = json.loads(d)
            prompt = prompts[int(params['promptId'])]
            article_dict['promptId'] = params['promptId']
            article_dict['prompt'] = prompt['prompt']
            article_dict['placeholder'] = prompt['placeholder']
    return article_dict

# Each time getTask is called, this is called--to store all the URL params here
def getParamsFromURL(request):
    # get parameters from URL
    params = {}
    for p in param_names:
        key = p
        val = request.get(p) if request.get(p) else None
        # special cases
        numeric_vals = ['task','promptId','amazon_articleId','amazon_promptId','apple_articleId','apple_promptId','uber_articleId','uber_promptId']
        if key in numeric_vals and val: 
            params[key] = int(val)
        elif key == 'newsfeed' and val: 
            params[key] = True if val=="true" or val=="True" else False
        else: # default: string
            params[key] = val
    return params

# Translating necessary params to URLs
def paramstoURL(params):
    string = ""
    # remove redundant params (don't need to pass to URL)
    for p in redundant_params:
        if p in params:
            del params[p]
    for p in params:
        if params[p] != None:
            string = string + "&"+ p +"="+ str(params[p])
    print(string)
    return string



def getNextLink(targetLink,params):
    params['task'] = getNextTask(params['task'])
    # params['curr_cat'] = getNextCategory(params['task'],params['curr_cat'])
    paramsForURL = paramstoURL(params)
    targetLink += 'getTask?'+ paramsForURL
    return targetLink

# Just a repeat print statment
def checkParams(params):
    print("##################################### PARAMS ")
    for p in params:
        if params[p] != None:
            print(p+' ==== '+str(params[p]))
    print("#####################################")

#and condition=nals. 
def checkPrereq(prereq,params):
    a_ok = True
    for p in prereq:
        if params[p] is None:
            return False
    return a_ok
