from flask import Flask, render_template, request, url_for, make_response
import sys

#This allows us to specify whether we are pushing to the sandbox or live site.
DEV_ENVIROMENT_BOOLEAN = True
if DEV_ENVIROMENT_BOOLEAN:
    amazon_host = "https://workersandbox.mturk.com/mturk/externalSubmit"
else:
    amazon_host = "https://www.mturk.com/mturk/externalSubmit"
app = Flask(__name__)

@app.route('/')
def welcome():
	# userAgreement()
	# createHIT()
	return render_template("intro.html")

@app.route('/logResults')
def logResults():
	# do something with results here
	return 'LOG'

@app.route('/getTask/<articleID>/<annotationID>', methods=['GET','POST'])
def getHIT(articleID, annotationID):
	# if request.args.get('assignmentId') == "ASSIGNMENT_ID_NOT_AVAILABLE":
	# 	pass # worker hasn't accepted task yet
	# else:
	# 	pass

    # TO DO
    # define article topic, annotation type, article.
	data = {
		"amazon_host": amazon_host,
		"hitID": request.args.get('hitId'),
		"workerID": request.args.get('workerId'),
		"assignmentID": request.args.get('assignmentId'),
		"turkSubmitTo": request.args.get('turkSubmitTo'),
		"workerID": request.args.get('workerId'),
		# "article_topic": article_topic,
		# "annotation_type": annotation,
		"article": getArticle(articleID),
        "annotation": annotationID
	}
    # log_task(data)
	response = make_response(render_template("task.html", data = data))

    # #This is particularly nasty gotcha.
    # #Without this header, your iFrame will not render in Amazon
    # response.headers['x-frame-options'] = 'this_can_be_anything'

	return response # article=article)

def getArticle(articleID):

	f = open('static/articles/test.txt', 'r')
	data = f.readlines()
	f.close()
	return data

# # Log before complete?
# def log_task(data):
#     hitID =data['hitId']
#     workerID =data['workerId']
#     assignmentID =data['assignmentId']
#     turkSubmitTo =data['turkSubmitTo']
#     workerID =data['workerId']
#     # TBContd
#     return
