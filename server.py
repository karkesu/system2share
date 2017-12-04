from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from config import *
from urllib.parse import urlencode
import sys, os, random, json

# TODO: make sure annotations show in the news feed, and that they are stored in the database
# make sure the right articles are shown
# and that the right articleIDs are stored in the database, basically a sanity check on the data

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

# Mostly used for populating variants
poss_assignments = {
    'newsFeedOrder': ['12','21'],
    'promptId': ['0', '1' ,'2', '3'],
    'articleId': ['1', '2'],
}

# Database Models
class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignmentId = db.Column(db.String(50), nullable=False)
    workerId = db.Column(db.String(50), nullable=False)
    step = db.Column(db.Integer, nullable=False)
    showNewsFeed = db.Column(db.Boolean, nullable=False)
    newsFeedOrder = db.Column(db.String(2), nullable=True)
    promptId = db.Column(db.Integer, nullable=False)
    amazon_newsfeed_annotation_a1 = db.Column(db.Integer, nullable=True)
    amazon_annotation_content_a1 = db.Column(db.String(1000), nullable=True)
    amazon_newsfeed_annotation_a2 = db.Column(db.Integer, nullable=True)
    amazon_annotation_content_a2 = db.Column(db.String(1000), nullable=True)
    amazon_articleId = db.Column(db.Integer, nullable=True)
    amazon_time_reading = db.Column(db.String(20), nullable=True)
    amazon_time_writing = db.Column(db.String(20), nullable=True)
    amazon_annotation = db.Column(db.String(1000), nullable=True)
    amazon_likert_summary_evaluation = db.Column(db.Integer, nullable=True)
    amazon_likert_prior_knowledge = db.Column(db.Integer, nullable=True)
    amazon_likert_learning = db.Column(db.Integer, nullable=True)
    apple_newsfeed_annotation_a1 = db.Column(db.Integer, nullable=True)
    apple_annotation_content_a1 = db.Column(db.String(1000), nullable=True)
    apple_newsfeed_annotation_a2 = db.Column(db.Integer, nullable=True)
    apple_annotation_content_a2 = db.Column(db.String(1000), nullable=True)
    apple_articleId = db.Column(db.Integer, nullable=True)
    apple_time_reading = db.Column(db.String(20), nullable=True)
    apple_time_writing = db.Column(db.String(20), nullable=True)
    apple_annotation = db.Column(db.String(1000), nullable=True)
    apple_likert_summary_evaluation = db.Column(db.Integer, nullable=True)
    apple_likert_prior_knowledge = db.Column(db.Integer, nullable=True)
    apple_likert_learning = db.Column(db.Integer, nullable=True)
    uber_newsfeed_annotation_a1 = db.Column(db.Integer, nullable=True)
    uber_annotation_content_a1 = db.Column(db.String(1000), nullable=True)
    uber_newsfeed_annotation_a2 = db.Column(db.Integer, nullable=True)
    uber_annotation_content_a2 = db.Column(db.String(1000), nullable=True)
    uber_articleId = db.Column(db.Integer, nullable=True)
    uber_time_reading = db.Column(db.String(20), nullable=True)
    uber_time_writing = db.Column(db.String(20), nullable=True)
    uber_annotation = db.Column(db.String(1000), nullable=True)
    uber_likert_summary_evaluation = db.Column(db.Integer, nullable=True)
    uber_likert_prior_knowledge = db.Column(db.Integer, nullable=True)
    uber_likert_learning = db.Column(db.Integer, nullable=True)


# Test View
@app.route('/')
def test():
    return '279akz'

# Submit Views
@app.route('/submitNewsFeed/<articleId>', methods=['GET'])
def submitNewsFeed(articleId):
    workerId = request.args.get('workerId')
    exp = Experiment.query.filter_by(workerId=workerId).first()
    if exp.step == 1:
        exp.amazon_articleId = articleId
    if exp.step == 4:
        exp.apple_articleId = articleId
    if exp.step == 7:
        exp.uber_articleId = articleId

    advanceExperiment(exp)
    return redirect(url_for('getHIT', workerId=workerId))

@app.route('/submitArticle', methods=['POST'])
def submitArticle():
    workerId = request.form.get('workerId')
    exp = Experiment.query.filter_by(workerId=workerId).first()

    annotation = request.form.get('annotation')
    readingTime = request.form.get('readingTime')
    writingTime = request.form.get('writingTime')

    # Amazon
    if exp.step == 2:
        exp.amazon_annotation = annotation
        exp.amazon_time_reading = readingTime
        exp.amazon_time_writing = writingTime

    # Apple
    if exp.step == 5:
        exp.apple_annotation = annotation
        exp.apple_time_reading = readingTime
        exp.apple_time_writing = writingTime

    # Uber
    if exp.step == 8:
        exp.uber_annotation = annotation
        exp.uber_time_reading = readingTime
        exp.uber_time_writing = writingTime

    advanceExperiment(exp)
    return redirect(url_for('getHIT', workerId=workerId))

@app.route('/submitReview', methods=['POST'])
def submitReview():
    workerId = request.form.get('workerId')
    exp = Experiment.query.filter_by(workerId=workerId).first()

    summary_evaluation = request.form.get('summary_evaluation')
    prior_knowledge = request.form.get('prior_knowledge')
    learning = request.form.get('learning')

    if exp.step == 3:
        exp.amazon_likert_summary_evaluation = summary_evaluation
        exp.amazon_likert_prior_knowledge = prior_knowledge
        exp.amazon_likert_learning = learning

    if exp.step == 6:
        exp.apple_likert_summary_evaluation = summary_evaluation
        exp.apple_likert_prior_knowledge = prior_knowledge
        exp.apple_likert_learning = learning

    if exp.step == 9:   
        exp.uber_likert_summary_evaluation = summary_evaluation
        exp.uber_likert_prior_knowledge = prior_knowledge
        exp.uber_likert_learning = learning 

    advanceExperiment(exp)
    return redirect(url_for('getHIT', workerId=workerId))

# Main HIT View

@app.route('/getTask/', methods=['GET','POST'])
def getHIT():

    # Before HIT is picked up, show consent form
    if request.args.get('assignmentId') == 'ASSIGNMENT_ID_NOT_AVAILABLE':
        return make_response(render_template('consent.html'))
    
    assignmentId = request.args.get('assignmentId')
    workerId = request.args.get('workerId')

    # Get database row corresponding to this worker
    exp = Experiment.query.filter_by(workerId=workerId).first()
    
    # If worker is seen for the first time, set up experiment
    if exp is None:
        exp = Experiment(
            workerId=workerId, 
            assignmentId=assignmentId,
            step=0,
            showNewsFeed=showNewsFeed(),
            promptId = getLeastFrequent('promptId', poss_assignments['promptId']),
            newsFeedOrder = getLeastFrequent('newsFeedOrder', poss_assignments['newsFeedOrder'])
            )
        db.session.add(exp)
        db.session.commit()
        advanceExperiment(exp)

    # set article category
    category = ''
    if exp.step < 4:
        category = 'amazon'
    elif exp.step < 7:
        category = 'apple'
    else:
        category = 'uber'

    # handle each step of the experiment

    # Amazon NewsFeed
    if exp.step == 1:
        if exp.showNewsFeed:
            return renderNewsFeedStep(exp, category)
        else:
            advanceExperiment(exp)

    # Amazon Article
    if exp.step == 2:
        if exp.amazon_articleId == None:
            exp.amazon_articleId = getArticleId(category)
            db.session.commit()
        return renderArticleStep(exp, category, exp.amazon_articleId)
   
    # Amazon Review
    if exp.step == 3:
        return renderReviewStep(exp, category)
    
    # Apple NewsFeed
    if exp.step == 4:
        if exp.showNewsFeed:
            return renderNewsFeedStep(exp, category)
        else:
            advanceExperiment(exp)
    
    # Apple Article
    if exp.step == 5:
        if exp.apple_articleId == None:
            exp.apple_articleId = getArticleId(category)
            db.session.commit()
        return renderArticleStep(exp, category, exp.apple_articleId)
    
    # Apple Review
    if exp.step == 6:
        return renderReviewStep(exp, category)
    
    # Uber NewsFeed
    if exp.step == 7:
        if exp.showNewsFeed:
            return renderNewsFeedStep(exp, category)
        else:
            advanceExperiment(exp)
    
    # Uber Article
    if exp.step == 8:
        if exp.uber_articleId == None:
            exp.uber_articleId = getArticleId(category)
            db.session.commit()
        return renderArticleStep(exp, category, exp.uber_articleId)
    
    # Uber Review
    if exp.step == 9:
        return renderReviewStep(exp, category)

    # Complete Experiment
    if exp.step >= 10:
        data = urlencode(exp.__dict__)
        print(exp.__dict__)
        return redirect(amazon_host + '?' + data, code=307)

    # It should never get here
    return 'You have completed the task'

def getLeastFrequent(param, options, additional_info=None):
    # for counterbalancing our experiements
    # e.g. param = 'promptId', options = ['0','1','2','3'],additional_info=None)
    # e.g. param = 'newsfeed_order', options = ['1,2','2,1'],additional_info=None)
    # e.g. param = 'amazon_articleId', options = ['0','1'],additional_info={'promptId':3})
    counts = {}
    for option in options:
        args = {param:option}
        if additional_info:
            for a in additional_info:
                args[a] = additional_info[a]
        counts[option] = Experiment.query.filter_by(**args).count()
    return min(counts, key=counts.get)

def getRandomAnnotation(category, promptId, articleId):
    # return actual annotation if there is one; otherwise ''
    cat_annotation = category+"_annotation"
    cat_articleId = category+"_articleId"
    args = { cat_articleId: articleId, 'promptId': promptId }
    all_annotations = Experiment.query.filter_by(**args).all()
    if len(all_annotations)>0:
        selected_annotation = all_annotations[0]
        return eval('selected_annotation.' + cat_annotation)
    else:
        print("category =  "+str(category))
        print("promptId =  "+str(promptId))
        print("articleId =  "+str(articleId))
        return None
    
    print(" cat_annotation ==================="+str(cat_annotation))
    print(" all_annotations ==================="+str(all_annotations))

# TODO: this needs to change to actually get annotaions, it's not getting anything at the moment
# This is probably a bit opaque..Basically generating and populating summaries & annotations from other users
def setNewsfeedContent(exp, category, newsFeedOrder):
    # Get newsfeed summaries content
    summaries_dict = {}
    for articleId in [exp.newsFeedOrder[0],exp.newsFeedOrder[1]]:
        annotation_num = category +"_annotation_content_a"+articleId
        annotationId = getLeastFrequent(annotation_num,poss_assignments['promptId'],{'newsFeedOrder':exp.newsFeedOrder})
        annotation_content = getRandomAnnotation(category,annotationId, articleId)
        article = getArticle(category , articleId)
        summaries_dict[articleId] = {}
        summaries_dict[articleId]['submitLink'] = request.url_root[:-1] + '/submitNewsFeed/' + articleId + '?workerId=' + exp.workerId
        summaries_dict[articleId]['title'] = article[0]
        summaries_dict[articleId]['byLine'] = article[1]
        summaries_dict[articleId]['preview'] = article[2:3][0][:150]+"..."
        summaries_dict[articleId]['annotation'] = annotation_content
        print(" annotation_num ==================="+str(annotation_num))
        print(" annotationId ==================="+str(annotationId))
        print(" annotation_content ==================="+str(annotation_content))

    return summaries_dict

# TODO: this is just a bogus function need to fix
def showNewsFeed():
    # return True # TESTING
    submissions = Experiment.query.all()
    # Don't show newsfeed if there are less than 5 total entries
    if len(submissions) < 5:
        return False
    else:
        for cat in ['amazon','apple','uber']:
            cat_articleId = cat+'_articleId'
            counts = []
            for option in [1,2]:
                for promptId in poss_assignments['promptId']:
                    args = {cat_articleId: option, 'promptId':promptId}
                    count = Experiment.query.filter_by(**args).count()
                    # if total submissions < 1 for any given articleId, don't show newsfeed
                    if count < 1:
                        return False
                    counts.append(count)
            # if there's a large (>5) difference in number of submissions for two articleIds within the same category, don't show newsfeed
            if max(counts)-min(counts)>5:
                return False

    return True # if everything passes


def renderNewsFeedStep(exp, category):
    summaries = setNewsfeedContent(exp, category, exp.newsFeedOrder)
    data = {}
    data['summaries'] = summaries
    return make_response(render_template('newsfeed.html', data=data))

def getArticleId(category):
    expVar = category + '_articleId'
    return getLeastFrequent(expVar, poss_assignments['articleId'])

def getArticle(articleCategory, articleId):
    f = open('static/articles/' + articleCategory + '/' + articleId + '.txt', 'r', encoding='utf-8')
    data = f.readlines()
    f.close()
    return data

def renderArticleStep(exp, category, articleId):
    articleId = str(articleId)
    article = getArticle(category, articleId)
    data = {}
    data['articleTitle'] = article[0]
    data['articleByLine'] = article[1]
    data['articleText'] = article[2:]
    data['workerId'] = request.args.get('workerId')
    data['submitURL'] = request.url_root + 'submitArticle'
    with open('static/articles/annotations.json') as json_file:
        d = "["+ str(json_file.read())+"]"
        prompts = json.loads(d)
        prompt = prompts[exp.promptId]
        data['prompt'] = prompt['prompt']
        data['placeholder'] = prompt['placeholder']

    return make_response(render_template('article.html', data=data))

# TODO: I think you mean to show only one summary in here and I'm showing both? Please edit if need be
def renderReviewStep(exp, category):
    data = {}
    data['workerId'] = request.args.get('workerId')
    data['submitURL'] = request.url_root + 'submitReview'
    if exp.showNewsFeed:
        summaries = {}
        if exp.step == 3:
            articleId = exp.amazon_articleId
        elif exp.step == 6:
            articleId = exp.apple_articleId
        else:
            articleId = exp.uber_articleId
        articleId = str(articleId)
        summary = {}
        article = getArticle(category, articleId)
        summary['title'] = article[0]
        summary['byLine'] = article[1]
        summary['preview'] = article[2:3][0][:150]+"..."
        summary['annotation'] = eval('exp.' + category + '_annotation_content_a' + articleId)
        summaries[articleId] = summary
        data['summaries'] = summaries
    return make_response(render_template('review.html', data=data))

def advanceExperiment(exp):
    exp.step += 1
    db.session.commit()
