import boto
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from dateutil.parser import *
import sys


def createHIT():
    # By default, HITs are created in the free-to-use Sandbox
    create_hits_in_live = False
#UPDATE THIS
    aws_access_key_id = 'AKIAJVHT5POJ4BDEGBNQ'
    aws_secret_access_key = '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'
    debug = 1
    reward = 0.05
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
        # debug=debug)

    external_question = ExternalQuestion('https://zeerak.net/279akz/getTask/', 500)
    # external_question = ExternalQuestion('https://cs279-final-project.herokuapp.com/find', 500)
    # question_html = open("templates/question.html", "r").read()

    response = mtc.create_hit(
        title='Share an article',
        keywords='read, react, share',
        description='Read a short article. How would you share this on Facebook?',
        duration=120,
        question=external_question,
        reward=reward,
        # response_groups='',
        )
    # The response included several fields that will be helpful later
    print("HELLOOO==============3")
    print(response)
    print(str(response[0]))
    # The response included several fields that will be helpful later
    hit_type_id = response[0].HITTypeId
    hit_id = response[0].HITId
    print("Your HIT has been created. You can see it at this link:")
    print("https://workersandbox.mturk.com/mturk/preview?groupId={}".format(hit_type_id))
    print("Your HIT ID is: {}".format(hit_id))
    print("\nAnd see results here:")
    print(mturk_environment['manage'])
      #
      # # client = boto.client(
      # #     service_name='mturk',
      # #     region_name='us-east-1',
      # #     endpoint_url=mturk_environment['endpoint'],
      # #     aws_access_key_id=aws_access_key_id,
      # #     aws_secret_access_key=aws_secret_access_key,
      # # )
      #
      # # The question we ask the workers is contained in this file.
      # question_sample = open("questions.xml", "r").read()
      #
      # # # Use qualifications to only use Workers who have had at least 80% of their assignments approved.
      # # worker_requirements = [{
      # #     'QualificationTypeId': '000000000000000000L0',
      # #     'Comparator': 'GreaterThanOrEqualTo',
      # #     'IntegerValues': [80],
      # #     'RequiredToPreview': True,
      # # }]
      #
      # # Create the HIT
      # response = client.create_hit(
      #     MaxAssignments=3,
      #     LifetimeInSeconds=600,
      #     AssignmentDurationInSeconds=600,
      #     Reward=mturk_environment['reward'],
      #     Title='Share an article',
      #     Keywords='read, react, share',
      #     Description='Read a short article. How would you share this on Facebook?',
      #     Question=ExternalQuestion("",500)
      #     # QualificationRequirements=worker_requirements, #as a Turker I'm not qualified to see this HIT lol..
      # )
      #
      # # theHIT = mtc.create_hit(question=q,
      # #                     lifetime=10 * 60 * 60, # 10 hours
      # #                     max_assignments=3,
      # #                     title=title,
      # #                     description=description,
      # #                     keywords=keywords,
      # #                     qualifications=qualifications,
      # #                     reward=pay,
      # #                     duration=120 * 60, # 120 minutes
      # #                     approval_delay=5 * 60 * 60, # 5 hours
      # #                     annotation=experimentName)
      #
      # # assert(theHIT.status == True)
      # # print theHIT
      # # print theHIT[0].HITId


    # In Sandbox this always returns $10,000. In live, it will be your acutal balance.
    # print("Your account balance is {}".format(client.get_account_balance()['AvailableBalance']))

    # The response included several fields that will be helpful later
    # hit_type_id = response['HIT']['HITTypeId']
    # hit_id = response['HIT']['HITId']
    # print("\nCreated HIT: {}".format(hit_id))

    # print("\nYou can work the HIT here:")
    # print(mturk_environment['preview'] + "?groupId={}".format(hit_type_id))
    #
    # print("\nAnd see results here:")
    # print(mturk_environment['manage'])


# PostHits()
