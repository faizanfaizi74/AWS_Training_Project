import json
import boto3
from boto3.dynamodb.conditions import Key

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# set environment variable
tableName = os.environ["URL_TABLE"]
table = dynamodb.Table(tableName)
    
# put existing items in table
for link in constants.URL_TO_MONITOR:
    table.put_item(
        Item={
            'Linkid': link
        }
    )

def lambda_handler(event, context):
    print(event)

    # Get the link
    link_id = event['body']

    # Get the method
    method = event['httpMethod']

    # pass the parameters
    api_call = post_get_put_delete(link_id, method)


def post_get_put_delete(link, method):
    # add methods for CRUD operations [ create/read/update/delete ]
    key = {'Linkid': link}

    #1. Get (Read) Item By Id
    if method == 'GET':
        response = table.get_item(
            Key=key
        )
        if response:
            return json_response(response)
        else:
            return json_response({"message": "URL not found"}, 404)

    #2. Post (Create) Item by Id
    elif method == 'POST':
        table.put_item(
            Item={'Linkid': link}
        )
        return json_response({"message": "Successfully added URL into the table"})

    #3. DELETE Item by Id
    elif method == 'DELETE':
        table.delete_item(
            Key=key
        )
        return json_response({"message": "Successfully deleted URL from the table"})

    #4. PUT (Update) Item by Id
    elif method == 'PUT':
        attribute_updates = {key: {'Value': value, 'Action': 'PUT'}
                             for key, value in request.form.items()}

        table.update_item(Key=key, AttributeUpdates=attribute_updates)

        return json_response({"message": "Successfully updated URL in the table"})

    else:
        return json_response({"message": "Invalid Method"})

def json_response(data, response_code=200):
    return json.dumps(data), response_code, {'Content-Type': 'application/json'}