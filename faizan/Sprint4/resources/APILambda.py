#-------------------------------------- Incomplete Code ---------------------------------#

import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    
    print(event)

    # # Get the service resource.
    # dynamodb = boto3.resource('dynamodb')

    # # set environment variable
    # tableName = os.environ["API_TABLE"]
    # table = dynamodb.Table(tableName)

    # # create/read/update/delete
    # message = json.loads(event['Records'][0]['Sns']['Message'])

    # # put item in table
    # table.put_item(
    #     Item={
    #         'MetricName': message["Trigger"]["MetricName"],
    #         'Timestamp': event['Records'][0]['Sns']['Timestamp'],
    #         'URL': message["Trigger"]["Dimensions"][0]["value"],
    #     },

    # )

    # #1. Example - Get Item By Id
	# response = table.get_item(
	# 	Key={
    #         'MetricName': message["Trigger"]["MetricName"],
    #         'Timestamp': event['Records'][0]['Sns']['Timestamp']
	# 	}
	# )
	# print(response['Item'])