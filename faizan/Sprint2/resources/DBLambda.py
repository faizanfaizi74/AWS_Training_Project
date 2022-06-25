import boto3
import json
import os

tablename = os.environ["Alarm_key"]
dynamodb = boto3.client('dynamodb')


def lambda_handler(event, context):
    # alarm information in JSON format
    # parse information to put in DB

    for record in event['Records']:

        message = json.loads(record['Sns']['Message'])
        item = {
            "AlarmName": {'S': message["AlarmName"]},
            "NewStateReason": {'S': message["NewStateReason"]},
            "Region": {'S': message["Region"]},
            
        }
        response = dynamodb.put_item(
            TableName = tablename,
            Item = item
        )
    print(event)
    return response