import json
import constants as constants
import boto3
import os
from datetime import datetime

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# set environment variable
tableName = os.environ["RESPONSE_TABLE"]
table = dynamodb.Table(tableName)

#################################   API Operations   ################################

def lambda_handler(event, context):
    # body = [{"event1":{"attr1": 897}}]
    # # Get the method
    
    method = event['httpMethod']
    body = event['body']
    #requestTime = event['requestContext']['requestTime']
    now = datetime.now()
    iso_date = now.isoformat()

    if method == 'POST':
        # Get the val
        json_obj = json.loads(body)
        value = int(json_obj[0]['event1']['attr1'])
        
        key = {
            "attr1": str(value),
            "requestTime": iso_date,
        }

        response = table.put_item(
            Item=key,
        )
        if response:
            return json_response({"message": "Successfull..!!"})
        else:
            return json_response({"message": "Invalid Response..Try Again!"})

    elif method == 'GET':
        items = table.scan()['Items']

        myList = []
        for i in range(len(items)):
            myList.append((items[i]['attr1'], items[i]['requestTime']))
        
        myList.sort(reverse=True)

        if len(myList) > 10:
            response = myList[:10]
        else:
            response = myList

        if response:
            return json_response(response)
        else:
            return json_response({"message": "Table is Empty"})

    else:
        return json_response({"message": "Invalid Method..Try Again!"})

def json_response(data):
    return {
        "statusCode": 200,
        "body": json.dumps(data),
        "headers": {'Content-Type': 'application/json'},
    }