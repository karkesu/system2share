import boto
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
import sys
import os

IS_DEV_ENVIRONMENT = False;
AWS_ACCESS_KEY_ID = os.environ['ACCESS_KEY']
AWS_SECRET_ACCESS_KEY = os.environ['SECRET_ACCESS_KEY']

environments = {
  "live": {
      "endpoint": "mechanicalturk.sandbox.amazonaws.com",
      "preview": "https://www.mturk.com/mturk/preview",
      "manage": "https://requester.mturk.com/mturk/manageHITs",
  },
  "sandbox": {
      "endpoint": "mechanicalturk.sandbox.amazonaws.com",
      "preview": "https://workersandbox.mturk.com/mturk/preview",
      "manage": "https://requestersandbox.mturk.com/mturk/manageHITs",
  },
}

mturk_environment = environments["live"] if IS_DEV_ENVIRONMENT else environments["sandbox"]

mtc = MTurkConnection(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    host=mturk_environment['endpoint'])


def createHIT(articleCategory, articleID):

    url = 'https://zeerak.net/279akz/getTask/'
    url += articleCategory
    url += '/'
    url += articleID
    external_question = ExternalQuestion(url, 500)

    response = mtc.create_hit(
        question=external_question,
        title='Share an article',
        keywords='read, react, share',
        description='Read a short article. How would you share this on Facebook?',
        duration=6000,
        max_assignments=100,
        reward=0.05,
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

def createManyHITs():
    for i in range(1,2):
        createHIT('education-system', str(i))

def deleteAllHITs():
    for hit in list(mtc.get_all_hits()):
        mtc.disable_hit(hit.HITId)
