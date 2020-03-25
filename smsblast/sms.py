import os
import re
import boto3

sns = boto3.client('sns')
topic = os.environ['SMS_TOPIC']

Exception = sns.exceptions.ClientError


def add(number):
    number = '+1' + re.sub('[^0-9]', '', number)
    sns.subscribe(
        TopicArn=topic,
        Protocol='sms',
        Endpoint=number
    )

def list_numbers():
    response = sns.list_subscriptions_by_topic(TopicArn=topic)
    for sub in response['Subscriptions']:
        attrs = sns.get_subscription_attributes(
            SubscriptionArn=sub['SubscriptionArn']
        )
        yield {
            'number': sub['Endpoint'],
            'arn': sub['SubscriptionArn'],
            'active': attrs['Attributes']['PendingConfirmation'] == 'false'
        }

def remove(number):
    for nm in list_numbers():
        if nm['number'] == number:
            sns.unsubscribe(SubscriptionArn=nm['arn'])
            return True
    return False
    
def send(message):
    response = sns.publish(
        TopicArn=topic,
        Message=message
    )
    return response['MessageId']

