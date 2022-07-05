#-------------------------------------- Incomplete Code ---------------------------------#

import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    tableName = os.environ["URL_TABLE"]
    table = dynamodb.Table(tableName)

    # create/read/update/delete

    # Get Method
    #1. Parse out query string params.
    message = json.loads(event['Records'][0]['Sns']['Message'])
    url = message["Trigger"]["Dimensions"][0]["value"]

    print("URL: " + url)

    #2. Construct the body of the response object
    urlResponse = {}
    urlResponse['url'] = url
    urlResponse['message'] = 'Successful..!!'

    #3. Construct http response object
    responseObject = {}
    responseObject['statusCode'] = 200      # OK 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(urlResponse)
 
    #4. Return the response object
    return responseObject


    #1. Example - Get Item By Id
	response = table.get_item(
		Key={
            'MetricName': message["Trigger"]["MetricName"],
            'Timestamp': event['Records'][0]['Sns']['Timestamp']
		}
	)
	print(response['Item'])