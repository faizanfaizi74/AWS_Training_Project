import json
import constants as constants
import boto3
import os

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# set environment variable
tableName = os.environ["RESPONSE_TABLE"]
table = dynamodb.Table(tableName)

#################################   API Operations   ################################

def lambda_handler(event, context):
    print("Event: ", event)
    # # Get the method
    method = event['httpMethod']
    requestTime = event["requestTime"]
    body = event['body']

    print("Body: ", body)
    print("RequestTime: ", requestTime)

    # Get the val
    json_obj = json.loads(body)
    value = int(json_obj[0]['event1']['attr1'])

    # key = [{"event1":{"attr1": 897}}]
    print({"ResponseValue": value})                 

    key = {
        "attr1": str(value),
        "requestTime": requestTime,
    }
    if method == 'POST':
        response = table.put_item(
            Item=key,
        )
        if response:
            return json_response({"message": "Successfull..!!"})
        else:
            return json_response({"message": "Invalid Response..Try Again!"})

    elif method == 'GET':
        response = table.scan(Limit=10)['Items']
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