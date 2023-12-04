import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


sqs = boto3.client('sqs')
queue_url = 'YOUR_SQS_QUEUE_URL'  

def lambda_handler(event, context):
    for record in event['Records']:
        if record['eventName'] == 'REMOVE':
            reminder = record['dynamodb']['OldImage']
            message_body = {
                'userId': reminder['userId']['S'],
                'message': reminder['message']['S'],
                'notificationType': reminder['notificationType']['S']
            }
            sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message_body))
            logger.info(f"Sent message to SQS: {message_body}")

    return {
        'statusCode': 200,
        'body': json.dumps('Messages sent to SQS successfully')
    }