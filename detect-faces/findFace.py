import boto3
import json

collectionId = 'ninjavas'

client = boto3.client('rekognition', 'us-east-1')

find_rsp = client.search_faces_by_image(
    Image={
        'S3Object': {
            'Bucket': 'ninjava-face-reg',
            'Name': 'RDWP3150.JPG'
        }
    },
    CollectionId = collectionId,
    FaceMatchThreshold = 0,
    MaxFaces=10
)

face_matches = find_rsp['FaceMatches']

faceCount = len(face_matches)

print('matches = ' + str(faceCount))

if(faceCount > 0):
    for match in face_matches:
        print(json.dumps(match, indent=2))
        face = match['Face']
        print('    Face Match = ' + face['ExternalImageId'])
    