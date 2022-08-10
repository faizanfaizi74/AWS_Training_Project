import json
from CloudwatchPutMetric import CloudwatchPutMetric
import constants as constants

#################################   API Operations   ################################

def lambda_handler(event, context):
    # # Get the method
    method = event['httpMethod']
    body = event['body']
    
    # Get the val
    value = int(json.loads(body)['arg1'])

    print({"ResponseValue": value})
    print(type(value))             # key = {"arg1": 1}
    
    # Post value to CloudWatch
    cw = CloudwatchPutMetric()

    if method == 'POST':
        dimension = [{'Name': 'arg1','Value': str(value)}]
        
        responseAvail = cw.put_data(constants.VALUE_MONITOR_NAMESPACE,
        constants.VALUE_MONITOR_NAME_RESPONSE,
        dimension, value)
        return json_response({"message": "Successfully Posted Value"})
    else:
        return json_response({"message": "Invalid Allowed!"})


def json_response(data):
    return {
        "statusCode": 200,
        "body": json.dumps(data),
        "headers": {'Content-Type': 'application/json'},
    }