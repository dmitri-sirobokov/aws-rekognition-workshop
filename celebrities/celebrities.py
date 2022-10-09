import boto3
import json

import PIL.ImageDraw
import PIL.Image

def draw_box(draw, boundingBox, width, linecolor):
    boxLeft = float(boundingBox['Left'])
    boxTop = float(boundingBox['Top'])
    boxWidth = float(boundingBox['Width'])
    boxHeight = float(boundingBox['Height'])

    imageWidth = myimage.size[0]
    imageHeight = myimage.size[1]
    rectX1 = imageWidth * boxLeft
    rectX2 = imageHeight * boxTop
    rectY1 = rectX1 + (imageWidth * boxWidth)
    rectY2 = rectX2 + (imageHeight * boxHeight)

    for i in range(0, width):
        draw.rectangle(((rectX1 + i, rectX2 + i), (rectY1 - i, rectY2 - i)), fill = None, outline = linecolor)

bucket = "rekognition-ninjava-unconference"
filename = "jumanji.jpeg"

client = boto3.client('rekognition', 'eu-central-1')
s3_resource = boto3.resource('s3')

s3_resource.Bucket(bucket).download_file(filename, 'input.jpeg')


response = client.recognize_celebrities(Image = {
    'S3Object': {
        'Bucket': bucket,
        "Name": filename
    }
})

celebrityFaces = response['CelebrityFaces']
unrecognizedFaces = response['UnrecognizedFaces']
draw = {}

with PIL.Image.open('input.jpeg') as myimage:
    draw = PIL.ImageDraw.Draw(myimage)
    for celebrityFace in celebrityFaces:
        print(celebrityFace['Name'])
        face = celebrityFace['Face']
        boundingBox = face['BoundingBox']
        print(boundingBox)
        draw_box(draw, boundingBox, 4, 'red')

        text_x = myimage.size[0] * float(boundingBox['Left']) + 5
        text_y = myimage.size[1] * float(boundingBox['Top']) + 5
        draw.text((text_x, text_y), text='test', color='red')
    for unrecognizedFace in unrecognizedFaces:
        boundingBox = unrecognizedFace['BoundingBox']
        draw_box(draw, boundingBox, 4, 'black')

    myimage.save('modified.jpeg')