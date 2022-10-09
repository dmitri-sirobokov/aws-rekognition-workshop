import boto3


rek_client = boto3.client('rekognition', 'us-east-1')
s3_resource = boto3.resource('s3')

