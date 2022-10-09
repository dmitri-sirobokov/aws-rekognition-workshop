import boto3
import json

client = boto3.client('rekognition', 'us-east-1')

collectionID = 'ninjavas'

response =  client.list_faces(
    CollectionId = collectionID,
    MaxResults = 100)
    
print(json.dumps(response, indent=2))