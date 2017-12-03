import boto
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.qualification import Qualifications, PercentAssignmentsApprovedRequirement, NumberHitsApprovedRequirement, LocaleRequirement
import sys
import os

IS_DEV_ENVIRONMENT = True
AWS_ACCESS_KEY_Id = os.environ['ACCESS_KEY']
AWS_SECRET_ACCESS_KEY = os.environ['SECRET_ACCESS_KEY']

environments = {
  "live": {
      "endpoint": "mechanicalturk.amazonaws.com",
      "preview": "https://www.mturk.com/mturk/preview",
      "manage": "https://requester.mturk.com/mturk/manageHITs",
  },
  "sandbox": {
      "endpoint": "mechanicalturk.sandbox.amazonaws.com",
      "preview": "https://workersandbox.mturk.com/mturk/preview",
      "manage": "https://requestersandbox.mturk.com/mturk/manageHITs",
  },
}

mturk_environment = environments['sandbox'] if IS_DEV_ENVIRONMENT else environments['live']

mtc = MTurkConnection(
    aws_access_key_Id=AWS_ACCESS_KEY_Id,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    host=mturk_environment['endpoint'])

def createHIT(articleCategory, articleId):

    url = 'https://www.zeerak.net/279akz/test/'
    url += articleCategory
    url += '/'
    url += articleId
    external_question = ExternalQuestion(url, 800)

    qualifications = Qualifications()
    qualifications.add(LocaleRequirement("EqualTo","US"))
    # qualifications.add(PercentAssignmentsApprovedRequirement(comparator="GreaterThan", integer_value="80"))
    # qualifications.add(NumberHitsApprovedRequirement(comparator="GreaterThan", integer_value="50"))

    response = mtc.create_hit(
        title='Read a short article and learn something new!',
        keywords='read, react, share, news',
        description='How would you share this on social media? Just one task!',
        duration=1200,
        question=external_question,
        reward=0.10,
        max_assignments=20,
        # qualifications=qualifications,
        # response_groups='', # batches??
        )

    # The response included several fields that will be helpful later
    hit_type_Id = response[0].HITTypeId
    hit_Id = response[0].HITId
    available_balance = mtc.get_account_balance()

    print("-------------------------------------------------------")
    print("Your HIT has been created. You can see it at this link:")
    print(">>>>>> https://workersandbox.mturk.com/mturk/preview?groupId={}".format(hit_type_Id))
    print("Your HIT Id is: {}".format(hit_Id))
    print("And see results here:")
    print(">>>>>> {}".format(mturk_environment['manage']))
    print("Your account balance is {}".format(available_balance))
    print("-------------------------------------------------------")

    return

# createHIT('tech-hq', '1')
def createManyHITs():
    for i in range(1,4):
        createHIT('tech-hq', str(i))

def getAllHITIds():
    Ids = []
    for hit in list(mtc.get_all_hits()):
        Ids.append(hit.HITId)
    return Ids

def deleteAllHITs():
    for hit in getAllHITIds():
        mtc.dispose_hit(hit)

def expireAllHITs():
    for hit in getAllHITIds():
        mtc.expire_hit(hit)

def getAssignmentsForHIT(hitId):
    assignments = []
    page = 1
    while len(mtc.get_assignments(hitId, page_number=str(page))) > 0:
        assignments.extend(mtc.get_assignments(hitId, page_number=str(page)))
        page += 1
    return assignments

def getAllAssignments():
    responses = []
    for hit in getAllHITIds():
        responses.append(getAssignmentsForHIT(hit))
    return responses

def approveAssignment(assignmentId):
    mtc.approve_assignment(assignmentId)

def approveAllAssignments():
    for hit in getAllAssignments():
        for assignment in hit:
            approveAssignment(assignment.AssignmentId)

def allAssignmentsToTSV():
    result = ''

    result += 'HITId' + '\t'
    result += 'AssignmentId' + '\t'
    result += 'WorkerId' + '\t'
    result += 'AcceptTime' + '\t'
    result += 'SubmitTime' + '\t'
    result += 'articleCategory' + '\t'
    result += 'articleId' + '\t'
    result += 'promptId' + '\t'
    result += 'annotation' + '\t'
    result += 'readingTime' + '\t'
    result += 'writingTime' + '\t'
    result += 'totalTime' + '\t'
    result += 'annotationLength' + '\t'

    result = result[:-1]
    result += '\n'

    for hit in getAllAssignments():
        for assignment in hit:

            result += assignment.HITId + '\t'
            result += assignment.AssignmentId + '\t'
            result += assignment.WorkerId + '\t'
            result += assignment.AcceptTime + '\t'
            result += assignment.SubmitTime + '\t'

            articleCategory = assignment.answers[0][1].fields[0]
            articleId = assignment.answers[0][2].fields[0]
            promptId = assignment.answers[0][3].fields[0]
            annotation = assignment.answers[0][4].fields[0]
            readingTime = assignment.answers[0][5].fields[0]
            writingTime = assignment.answers[0][6].fields[0]
            totalTime = str(int(readingTime) + int(writingTime))
            annotationLength = str(len(annotation))

            result += articleCategory + '\t'
            result += articleId + '\t'
            result += promptId + '\t'
            result += annotation + '\t'
            result += readingTime + '\t'
            result += writingTime + '\t'
            result += totalTime + '\t'
            result += annotationLength + '\t'

            result = result[:-1]
            result += '\n'

    return result
