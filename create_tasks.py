import sys
import boto3


def createHIT():
    # By default, HITs are created in the free-to-use Sandbox
    create_hits_in_live = False
    aws_access_key_id = 'AKIAJVHT5POJ4BDEGBNQ'
    aws_secret_access_key = '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'

    environments = {
            "live": {
                "endpoint": "https://mturk-requester.us-east-1.amazonaws.com",
                "preview": "https://www.mturk.com/mturk/preview",
                "manage": "https://requester.mturk.com/mturk/manageHITs",
                "reward": "0.00"
            },
            "sandbox": {
                "endpoint": "https://mturk-requester-sandbox.us-east-1.amazonaws.com",
                "preview": "https://workersandbox.mturk.com/mturk/preview",
                "manage": "https://requestersandbox.mturk.com/mturk/manageHITs",
                "reward": "0.1"
            },
    }
    mturk_environment = environments["live"] if create_hits_in_live else environments["sandbox"]

    client = boto3.client(
        service_name='mturk',
        region_name='us-east-1',
        endpoint_url=mturk_environment['endpoint'],
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    # The question we ask the workers is contained in this file.
    question_sample = open("questions.xml", "r").read()

    # Use qualifications to only use Workers who have had at least 80% of their assignments approved.
    worker_requirements = [{
        'QualificationTypeId': '000000000000000000L0',
        'Comparator': 'GreaterThanOrEqualTo',
        'IntegerValues': [80],
        'RequiredToPreview': True,
    }]

    # Create the HIT
    response = client.create_hit(
        MaxAssignments=3,
        LifetimeInSeconds=600,
        AssignmentDurationInSeconds=600,
        Reward=mturk_environment['reward'],
        Title='Share an article',
        Keywords='read, react, share',
        Description='Read a short article. How would you share this on Facebook?',
        Question=question_sample,
        # QualificationRequirements=worker_requirements, #as a Turker I'm not qualified to see this HIT lol..
    )

    # In Sandbox this always returns $10,000. In live, it will be your acutal balance.
    print("Your account balance is {}".format(client.get_account_balance()['AvailableBalance']))

    # The response included several fields that will be helpful later
    hit_type_id = response['HIT']['HITTypeId']
    hit_id = response['HIT']['HITId']
    print("\nCreated HIT: {}".format(hit_id))

    print("\nYou can work the HIT here:")
    print(mturk_environment['preview'] + "?groupId={}".format(hit_type_id))

    print("\nAnd see results here:")
    print(mturk_environment['manage'])
