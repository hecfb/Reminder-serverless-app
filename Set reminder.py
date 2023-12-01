import json
import boto3
import logging
from datetime import datetime, timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Reminder_Table')


def lambda_handler(event, context):
    try:
        data = json.loads(event['body'])
        reminder_id = data['id']
        user_id = data['userId']
        ttl = int((datetime.now() + timedelta(days=1)).timestamp())
        notification_type = data['notificationType']
        message = data['message']
        response = table.put_item(
            Item={
                'id': reminder_id,
                'userId': user_id,
                'TTL': ttl,
                'notificationType': notification_type,
                'message': message
            }
        )

        logger.info(f"Set reminder: {response}")
        return {
            'statusCode': 200,
            'body': json.dumps('Reminder set successfully!')
        }
    except Exception as e:
        logger.error(f"Error setting reminder: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
