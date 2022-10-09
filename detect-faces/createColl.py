import boto3
import json

client = boto3.client('rekognition', 'us-east-1')
collectionID = 'ninjavas'

def add_facial_information(face_name: str, filename: str):
    index_rsp = client.index_faces(
        CollectionId = collectionID,
        Image = { 'S3Object': { 'Bucket': 'ninjava-face-reg', 'Name': filename }},
        ExternalImageId = face_name
    )
    print(face_name + '    added')
    
create_rsp = client.create_collection(CollectionId = collectionID)
retcode = create_rsp['StatusCode']
print('Status Code = ' + str(retcode))
if (retcode != 200):
    print('could not create collection')
    exit()
    
add_facial_information('Dmitri', 'dmitri-portrait.jpg')
