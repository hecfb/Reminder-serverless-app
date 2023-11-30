import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sns = boto3.client('sns')
ses = boto3.client('ses')


def lambda_handler(event, context):
    for record in event['Records']:
        if record['eventName'] == 'REMOVE':
            reminder = record['dynamodb']['OldImage']
            message = reminder['message']['S']
            notification_type = reminder['notificationType']['S']

            if notification_type == 'sms':
                sns.publish(
                    PhoneNumber=reminder['userId']['S'],
                    Message=message
                )
            elif notification_type == 'email':
                ses.send_email(
                    Source='from@example.com',
                    Destination={'ToAddresses': [reminder['userId']['S']]},
                    Message={
                        'Subject': {'Data': 'Reminder'},
                        'Body': {'Text': {'Data': message}}
                    }
                )

            logger.info(f"Sent reminder: {message}")

    return {
        'statusCode': 200,
        'body': json.dumps('Reminders sent successfully')
    }
