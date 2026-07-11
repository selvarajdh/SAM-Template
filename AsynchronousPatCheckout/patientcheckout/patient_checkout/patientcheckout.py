import boto3
import json
import os
import logging

s3 = boto3.client('s3')
snsclient = boto3.client('sns')
logger = logging.getLogger('patientcheckout')
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    topic = os.environ.get('PATIENT_CHECKOUT_TOPIC')
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    #print("Bucket name : ",bucket_name)
    file_key = event['Records'][0]['s3']['object']['key']
    logger.info('Reading {} from {}'.format(file_key, bucket_name))
    #print("file key name : ",file_key)
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)

    file_content= obj['Body'].read().decode('utf-8')
    checkout_events=json.loads(file_content)
    
    #print("checkout events : ",checkout_events)

    for each_event in checkout_events:
        logger.info('Message being published')
        logger.info(each_event)
        #print(each_event)
        snsclient.publish(
            TopicArn=topic,
            Message=json.dumps({'default':json.dumps(each_event)}),
            MessageStructure='json'
        )


        #snsclient.publish(
        #    TopicArn=topic,
        #    Message=json.dumps(each_event),
        #    MessageStructure='json'
        #)