import boto3
import json

client = boto3.client('rekognition')

response = client.detect_labels(Image={
    'S3Object': {
        'Bucket': 'rekognition-ninjava-unconference',
        'Name': 'cat.jpg'
    }
})


print(json.dumps(response, indent = 2))

for label in response['Labels']:
    print(label['Name'] + ' ' + ('%.1f' % label['Confidence']) + '%')