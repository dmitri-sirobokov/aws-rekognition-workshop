import boto3
import json
import utils
import PIL.ImageDraw
import PIL.Image
import PIL.ImageFont
import io

client=boto3.client('rekognition')
s3 = boto3.resource('s3')

def println(value):
    return value + '\n'
    
def printAge(face):
    return println('Age: ' + str(face['AgeRange']['Low']) + '-' + str(face['AgeRange']['High']))
    
def printConfidence(value):
    return ' ({0:.2f}%)'.format(value)
    
def printEmotion(face):
    return println('Emotion: ' + str(face['Emotions'][0]['Type']) + printConfidence(face['Emotions'][0]['Confidence']))
    
def printValueConf(face, name):
    return println(name + ': ' + str(face[name]['Value']) + printConfidence(face[name]['Confidence']))
    
    
def detect_faces(photo, bucket):

    font = PIL.ImageFont.truetype('courier.ttf', size=10)
    response = client.detect_faces(Image={'S3Object':{'Bucket':bucket,'Name':photo}},Attributes=['ALL'])
    
    with open('detectFaces.json', 'w') as f:
        f.write(json.dumps(response, indent=2))
        
    print('Detected faces for ' + photo)    
    index = 1;
    with PIL.Image.open(photo) as myimage:
        draw = PIL.ImageDraw.Draw(myimage)
        
        for faceDetail in response['FaceDetails']:
            print('Here are the other attributes:')
            print(json.dumps(faceDetail, indent=4, sort_keys=True))
            
            info_s = printAge(faceDetail) \
                + printValueConf(faceDetail, 'Gender') \
                + printEmotion(faceDetail) \
                + printValueConf(faceDetail, 'Smile') \
                + printValueConf(faceDetail, 'Beard') \
                + printValueConf(faceDetail, 'Eyeglasses')
                
    		# Access predictions for individual face details and print them
            with io.open(str(index) + '.txt', 'w') as f_face:
                f_face.write(info_s)
    		    
    		    
    		    
            print(info_s)
            println('')

            boundingBox = faceDetail['BoundingBox']
            
            utils.draw_box(draw, myimage, boundingBox, 4, 'red', info_s, font)
            index += 1
            
    myimage.save('modified-' + photo)

    return len(response['FaceDetails'])

photo='RDWP3150.JPG'
bucket='ninjava-face-reg'

s3.Bucket(bucket).download_file(photo, photo)

face_count=detect_faces(photo, bucket)
print("Faces detected: " + str(face_count))

