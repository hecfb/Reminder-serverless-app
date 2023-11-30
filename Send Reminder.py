import boto3
import json

def lambda_handler(event, context):
    sns = boto3.client('sns')
    ses = boto3.client('ses')

    for record in event['Records']:
        if record['eventName'] == 'REMOVE':
            attributes = record['dynamodb']['OldImage']
            
            if attributes['notificationType']['S'] == 'sms':
                sns.publish(
                    PhoneNumber=attributes['userId']['S'],
                    Message=attributes['message']['S']
                )
            elif attributes['notificationType']['S'] == 'email':
                # Code to send an email using SES goes here
                
    return {
        'statusCode': 200,
        'body': json.dumps('Reminder sent successfully')
    }
