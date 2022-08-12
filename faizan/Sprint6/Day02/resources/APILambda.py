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
    
    print("Event: ", event)
    # # Get the method
    
    method = event['httpMethod']
    requestTime = event['requestContext']['requestTime']
    now = datetime.now()
    iso_date = now.isoformat()
    body = event['body']

    print("Body: ", body)
    print("RequestTime: ", requestTime)

    if method == 'POST':
        # Get the val
        json_obj = json.loads(body)
        value = int(json_obj[0]['event1']['attr1'])
        
        print({"ResponseValue": value})
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
        response = table.scan(Limit=10)['Items']
        print(response)
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