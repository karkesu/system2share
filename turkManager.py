import boto
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.qualification import Qualifications, PercentAssignmentsApprovedRequirement, NumberHitsApprovedRequirement, LocaleRequirement
import sys
import os

IS_DEV_ENVIRONMENT = False
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

def createHIT():

    # TODO: fix height here
    url = 'https://www.zeerak.net/279akz/getTask/'
    external_question = ExternalQuestion(url, 1200)

    qualifications = Qualifications()
    qualifications.add(LocaleRequirement("EqualTo","US"))

    response = mtc.create_hit(
        title='Read a short article and learn something new!',
        keywords='read, react, share, news',
        description='How would you share this on social media? Just one task!',
        duration=1800,
        question=external_question,
        reward=0.30,
        max_assignments=5,
        qualifications=qualifications,
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
