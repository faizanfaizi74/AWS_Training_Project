import boto3
import json
import os

def lambda_handler(event, context):
    # alarm information in JSON format
    # parse information to put in DB

    dynamodb=boto3.resource('dynamodb', region_name='us-east-1')

    # Get the table name
    tablename = os.genenv("Alarm_key")
    table=dynamodb.Table(tablename)

    Message_ID = event['Records'][0]['Sns']['MessageId']
    timestamp = event['Records'][0]['Sns']['Timestamp']
    message  = event['Records'][0]['Sns']['Message']
    reason  = event['Records'][0]['Sns']['NewStateReason']
    region  = event['Records'][0]['Sns']['Region']

    #Adding the parameters to the table 
    table.put_item(
        Item={
            'AlarmID' : Message_ID,
            'AlarmTime' : timestamp,
            'Message' : message,
            'Reason' : reason,
            'Region' : region
        })

    print(event)
    return response