import json
import boto3
import logging
import decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Reminder_Table')


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            if obj % 1 == 0:
                return int(obj)
            else:
                return float(obj)
        return super(DecimalEncoder, self).default(obj)


def lambda_handler(event, context):
    user_id = event['queryStringParameters']['userId']
    response = table.query(
        IndexName='userId-TTL-index',
        KeyConditionExpression=boto3.dynamodb.conditions.Key(
            'userId').eq(user_id)
    )

    reminders = response.get('Items', [])
    formatted_reminders = [{
        'id': reminder['id'],
        'userId': reminder['userId'],
        'TTL': reminder['TTL'],
        'notificationType': reminder['notificationType'],
        'message': reminder['message']
    } for reminder in reminders]

    logger.info(f"Retrieved reminders: {formatted_reminders}")
    return {
        'statusCode': 200,
        'body': json.dumps(formatted_reminders, cls=DecimalEncoder)
    }
