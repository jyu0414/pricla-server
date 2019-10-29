#!/bin/env python
# coding: utf-8

import os
from PIL import Image
from io import *
from flask import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/',methods=["GET","POST"])
def index():
    if request.method == "GET":
        return "GET method is not available."

    elif request.method == "POST":

        #Init Layout
        docWidth = 1000
        docHeight = 1408
        xMargin = 50
        yMargin = 135
        xSep = 30
        ySep = 40
        imgWidth = 280
        imgHeight = 210
        xCount = 3
        yCount = 5

        #Get
        response = make_response()
        reqImage = Image.open(BytesIO(request.get_data()))
        frame = Image.open("frame"+request.headers.get("frame")+".png")

        #Make Image
        img = Image.new('RGB', (docWidth, docHeight), (255, 255, 255))
        (reqW, reqH) = reqImage.size
        reqNewWidth = int(imgHeight/reqH*reqW)
        reqImage = reqImage.resize((reqNewWidth,int(imgHeight)))
        (frameW, frameH) = frame.size
        frameNewWidth = int(imgHeight/frameH*frameW)
        frame = frame.resize((frameNewWidth,int(imgHeight)))
        #crop
        reqImage = reqImage.crop(((reqNewWidth - imgWidth)/2,0,imgWidth + (reqNewWidth - imgWidth)/2,imgHeight))
        frame = frame.crop(((frameNewWidth - imgWidth)/2,0,imgWidth + (frameNewWidth - imgWidth)/2,imgHeight))

        for x in range(xCount):
            for y in range(yCount):
                leftTopX = xMargin + x * (xSep + imgWidth)
                leftTopY = yMargin + y * (ySep + imgHeight)
                img.paste(reqImage,(leftTopX,leftTopY))
                img.paste(frame, (leftTopX,leftTopY),frame)

        #Submmit
        buf = BytesIO()
        img.save(buf, 'png')
        response = make_response(buf.getvalue())
        response.headers["Content-type"] = "image/png"
        response.headers["Content-Disposition"] = "attachment;filename=\"image.png\""
        return response

    return "error"


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)