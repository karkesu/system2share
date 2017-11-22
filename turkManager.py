import boto
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.qualification import Qualifications, PercentAssignmentsApprovedRequirement, NumberHitsApprovedRequirement, LocaleRequirement
import sys
import os

IS_DEV_ENVIRONMENT = False;
AWS_ACCESS_KEY_ID = os.environ['ACCESS_KEY']
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
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    host=mturk_environment['endpoint'])

def createHIT(articleCategory, articleID):

    url = 'https://www.zeerak.net/279akz/getTask/'
    url += articleCategory
    url += '/'
    url += articleID
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
        # qualifications=qualifications,
        max_assignments=20,
        # response_groups='', # batches??
        )

    # The response included several fields that will be helpful later
    hit_type_id = response[0].HITTypeId
    hit_id = response[0].HITId
    available_balance = mtc.get_account_balance()

    print("-------------------------------------------------------")
    print("Your HIT has been created. You can see it at this link:")
    print(">>>>>> https://workersandbox.mturk.com/mturk/preview?groupId={}".format(hit_type_id))
    print("Your HIT ID is: {}".format(hit_id))
    print("And see results here:")
    print(">>>>>> {}".format(mturk_environment['manage']))
    print("Your account balance is {}".format(available_balance))
    print("-------------------------------------------------------")

    return

# createHIT('tech-hq', '1')
def createManyHITs():
    for i in range(1,4):
        createHIT('tech-hq', str(i))

def getAllHITIDs():
    ids = []
    for hit in list(mtc.get_all_hits()):
        ids.append(hit.HITId)
    return ids

def deleteAllHITs():
    for hit in getAllHITIDs():
        mtc.disable_hit(hit)

def getAllAssignments(hitID):
    assignments = []
    page = 1
    while len(mtc.get_assignments(hitID, page_number=str(page))) > 0:
        assignments.extend(mtc.get_assignments(hit, page_number=str(page)))
        page += 1
    return assignments

def getAllResponses():
    responses = []
    for hit in getAllHITIDs():
        responses.append(getAllAssignments(hit))
    return responses
