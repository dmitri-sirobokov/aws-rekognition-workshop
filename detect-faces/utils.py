def draw_box(draw, myimage, bounding_box, width, line_color, name, font):
    boxLeft = float(bounding_box['Left'])
    boxTop = float(bounding_box['Top'])
    boxWith = float(bounding_box['Width'])
    boxHeight = float(bounding_box['Height'])
    imageWidth = myimage.size[0]
    imageHeight = myimage.size[1]
    rectX1 = imageWidth * boxLeft
    rectX2 = imageHeight * boxTop
    rectY1 = rectX1 + (imageWidth * boxWith)
    rectY2 = rectX2 + (imageHeight * boxHeight)
    
    for i in range(0, width):
        draw.rectangle(((rectX1 + i, rectX2 + i), (rectY1 - i, rectY2 - i)), fill=None, outline=line_color)
        
    draw.text((rectX1 + width, rectX2 + width), name, fill=(255,255,0), font=font)

        