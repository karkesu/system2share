import boto
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
import sys
import os


def createHIT(articleCategory, articleID):
    # By default, HITs are created in the free-to-use Sandbox
    create_hits_in_live = False
#UPDATE THIS
    aws_access_key_id = os.environ['access_key']
    aws_secret_access_key = os.environ['secret_access_key']
    print("access keys ---------------------------")
    print(aws_access_key_id)
    print(aws_secret_access_key)
    environments = {
      "live": {
          "endpoint": "mechanicalturk.sandbox.amazonaws.com",
          "preview": "https://www.mturk.com/mturk/preview",
          "manage": "https://requester.mturk.com/mturk/manageHITs",
      },
      "sandbox": {
          "endpoint": "mechanicalturk.sandbox.amazonaws.com",
          # "endpoint": "mturk-requester-sandbox.us-east-1.amazonaws.com",
          "preview": "https://workersandbox.mturk.com/mturk/preview",
          "manage": "https://requestersandbox.mturk.com/mturk/manageHITs",
      },
    }
    mturk_environment = environments["live"] if create_hits_in_live else environments["sandbox"]

    mtc = MTurkConnection(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        host=mturk_environment['endpoint'])

    url = 'https://zeerak.net/279akz/getTask/'
    url += articleCategory
    url += '/'
    url += articleID
    external_question = ExternalQuestion(url, 500)

    response = mtc.create_hit(
        title='Share an article',
        keywords='read, react, share',
        description='Read a short article. How would you share this on Facebook?',
        duration=120,
        question=external_question,
        reward=0.05,
        # response_groups='', # batches??
        )

    # The response included several fields that will be helpful later
    hit_type_id = response[0].HITTypeId
    hit_id = response[0].HITId
    available_balance = mtc.get_account_balance()

    print("-------------------------------------------------------")
    print(response[0])
    print("Your HIT has been created. You can see it at this link:")
    print(">>>>>> https://workersandbox.mturk.com/mturk/preview?groupId={}".format(hit_type_id))
    print("Your HIT ID is: {}".format(hit_id))
    print("And see results here:")
    print(">>>>>> {}".format(mturk_environment['manage']))
    # In Sandbox this always returns $10,000. In live, it will be your acutal balance.
    print("Your account balance is {}".format(available_balance))
    print("-------------------------------------------------------")

    return
for i in range(1,4):
    createHIT('tech-hq', str(i))
    # for a in range(10):
    #     createHIT('tech-hq', str(i))
# createHIT('tech-hq', articleID)
