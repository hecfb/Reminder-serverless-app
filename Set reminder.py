import boto3
import os
import json
import time

# Initialize a DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])


def lambda_handler(event, context):
    body = json.loads(event['body'])
    user_id = body['userId']
    ttl = int(time.time()) + body['delayInSeconds']
    notification_type = body['notificationType']
    message = body['message']

    table.put_item(
        Item={
            'userId': user_id,
            'TTL': ttl,
            'notificationType': notification_type,
            'message': message
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Reminder set successfully')
    }
