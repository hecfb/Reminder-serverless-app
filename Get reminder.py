import boto3
import os
import json
from boto3.dynamodb.conditions import Key

# Initialize a DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])


def lambda_handler(event, context):
    user_id = event['pathParameters']['userId']

    response = table.query(
        IndexName='UserIdAndTTLIndex',
        KeyConditionExpression=Key('userId').eq(user_id)
    )

    reminders = response['Items']
    formatted_reminders = [{'id': reminder['userId'],
                            'message': reminder['message']} for reminder in reminders]

    return {
        'statusCode': 200,
        'body': json.dumps(formatted_reminders)
    }
