import uvicorn
import fastapi
import base64
import io
import os
import sys
import yaml
import logging
import uuid
import time

from datetime import datetime

from starlette.requests import Request
from typing import List, Optional
from fastapi import FastAPI, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pdf_annotate import PdfAnnotator, Location, Appearance
from pdfrw import PdfReader

loggingConfigFile = "C:/inetpub/utilspython/logging.conf"
logging.config.fileConfig(loggingConfigFile, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

mainhandler = FastAPI()

UsersImageLocation = "C:/inetpub/wwwroot/Images/"
ConfigFileLocation = "C:/inetpub/utilspython/"

class IdentityDetails(BaseModel):
    encryptedUserId:str
    imageFileName:str
    name:str
    code:str

class AnnotationDetail(BaseModel):
    anType:str
    page:int
    #BoundingBox
    x:Optional[float] = None
    y:Optional[float] = None
    width:Optional[float] = None
    height:Optional[float] = None
    #IfText
    text:Optional[str] = None
    #Points Points if it line or highlight
    points:Optional[List[List[int]]] = None
    #Identification if it sign or initial or stamp
    identification:Optional[IdentityDetails] = None

class Item(BaseModel):
    pdffile:str
    annotations:List[AnnotationDetail]

@mainhandler.middleware("http")
async def log_requests(request: Request, call_next):
    reqTime = datetime.now().strftime("[%m/%d/%Y, %H:%M:%S]")
    logger.info(f"reqTime={reqTime}::path={request.url.path} client address={request.client.host}:request.client.port")
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"reqTime={reqTime} completed_in={formatted_process_time}ms status_code={response.status_code}")
    
    return response

@mainhandler.get("/")
async def root():
    return {"message":"Hello World"}

@mainhandler.get("/testImagePath")
async def testImagePath():
    return FileResponse(UsersImageLocation+"imageTester.png")

@mainhandler.post("/makepdf/")
async def makePdf(Item:Item):
    pdfBytes = base64.b64decode(Item.pdffile)
    reader = PdfReader(fdata=pdfBytes)
    annotator = PdfAnnotator(reader)
    for i in Item.annotations:
        if i.anType == "line":
            await addLine(annotator, i)
        elif i.anType == 'polyline':
            await addLine(annotator, i)
        elif i.anType == 'highlighter':
            await addHighlight(annotator, i)
        elif i.anType == 'highlighterPolyline':
            await addHighlight(annotator, i)
        elif i.anType == 'text':
            await addText(annotator, i)
        elif i.anType == 'identity':
            await addIdentity(annotator, i)
    # Creating file results
    fileid = uuid.uuid4()
    fileName = str(fileid)+".pdf"
    annotator.write(fileName)
    encoded_string = ""
    with open(fileName, "rb") as pdf_file:
        encoded_string = base64.b64encode(pdf_file.read())
    os.remove(fileName)
    return {"result":encoded_string}

async def addLine(pdf, annotationItem:AnnotationDetail):
    try:
        sizePapper= pdf.get_size(annotationItem.page - 1)
        # Penyesuaian titik coordinat (0,0) dan titik start line
        # karena di python leftbottom di javascript lefttop
        y = sizePapper[1] - annotationItem.y
        for idx in range(len(annotationItem.points)):
            point = annotationItem.points[idx]
            annotationItem.points[idx]= [point[0] + annotationItem.x, y - point[1]]
        pdf.add_annotation(
            'line',
            Location(points= annotationItem.points, page= annotationItem.page - 1),
            Appearance(stroke_color= (1, 0, 0), stroke_width= 4),
        )
    except Exception as e:
        #TODO print logging
        print(str(e))

async def addPolyLine(pdf, annotationItem:AnnotationDetail):
    try:
        sizePapper= pdf.get_size(annotationItem.page - 1)
        # Penyesuaian titik coordinat (0,0) dan titik start line
        # karena di python leftbottom di javascript lefttop
        y = sizePapper[1] - annotationItem.y
        for idx in range(len(annotationItem.points)):
            point = annotationItem.points[idx]
            annotationItem.points[idx]= [point[0] + annotationItem.x, y - point[1]]
        pdf.add_annotation(
            'polyline',
            Location(points= annotationItem.points, page= annotationItem.page - 1),
            Appearance(stroke_color= (1, 0, 0), stroke_width= 4),
        )
    except Exception as e:
        #TODO print logging
        print(str(e))

async def addHighlight(pdf, annotationItem:AnnotationDetail):
    try:
        sizePapper= pdf.get_size(annotationItem.page - 1)
        # Penyesuaian titik coordinat (0,0) dan titik start line
        # karena di python leftbottom di javascript lefttop
        y = sizePapper[1] - annotationItem.y
        for idx in range(len(annotationItem.points)):
            point = annotationItem.points[idx]
            annotationItem.points[idx]= [point[0] + annotationItem.x, y - point[1]]
        pdf.add_annotation(
            'line',
            Location(points= annotationItem.points, page= annotationItem.page - 1),
            Appearance(stroke_color= (1,1,0, 0.4), stroke_width= 12),
        )
    except Exception as e:
        #TODO print logging
        print(str(e))

async def addHighlightPolyline(pdf, annotationItem:AnnotationDetail):
    try:
        sizePapper= pdf.get_size(annotationItem.page - 1)
        # Penyesuaian titik coordinat (0,0) dan titik start line
        # karena di python leftbottom di javascript lefttop
        y = sizePapper[1] - annotationItem.y
        for idx in range(len(annotationItem.points)):
            point = annotationItem.points[idx]
            annotationItem.points[idx]= [point[0] + annotationItem.x, y - point[1]]
        pdf.add_annotation(
            'polyline',
            Location(points= annotationItem.points, page= annotationItem.page - 1),
            Appearance(stroke_color= (1,1,0, 0.4), stroke_width= 12),
        )
    except Exception as e:
        #TODO print logging
        print(str(e))

# YStart and YEnd need to reversed because data has the origin(0,0) located on on topleft, in this module origin is on bottomleft.
async def addText(pdf, annotationItem:AnnotationDetail):
    try:
        sizePapper= pdf.get_size(annotationItem.page - 1)
        xStart= annotationItem.x
        yStart= sizePapper[1] - (annotationItem.y)
        if annotationItem.width == 0:
            xEnd= sizePapper[0]
        else:
            xEnd= xStart + annotationItem.width
        yEnd= yStart - annotationItem.height
        textUsed= annotationItem.text
        pdf.add_annotation(
            'text',
            Location(x1= xStart, y1= yEnd, x2= xEnd, y2= yStart, page= annotationItem.page - 1),
            Appearance(fill= [1, 0, 0], stroke_width= 1, font_size= 9, content= textUsed),
        )
    except Exception as e:
        #TODO print logging
        print(str(e))

# USING SHARED STORAGE FOR IMAGE SEARCHING
# YStart and YEnd need to reversed because data has the origin(0,0) located on on topleft, in this module origin is on bottomleft.
async def addIdentity(pdf, annotationItem:AnnotationDetail):
    try:
        sizePapper= pdf.get_size(annotationItem.page - 1)
        xStart= annotationItem.x
        yStart= sizePapper[1] - (annotationItem.y)
        # Keep image ration at 1:1
        imageHeight = annotationItem.height * 0.8
        xEnd= xStart + imageHeight
        yEnd= yStart - (annotationItem.height * 0.8)
        imageLocation = UsersImageLocation +"/Member/"+ annotationItem.identification.encryptedUserId + "/" + annotationItem.identification.imageFileName
        pdf.add_annotation(
            'image',
            Location(x1= xStart, y1= yEnd, x2= xEnd, y2= yStart, page= annotationItem.page - 1),
            Appearance(stroke_width= 0, image= imageLocation),
        )
        xEnd= xStart + annotationItem.width + 5
        if xEnd > sizePapper[0]:
            xEnd == sizePapper[0]
        yStart= yStart - (annotationItem.height * 0.8)
        yEnd= yStart - (annotationItem.height * 0.2)
        textIdentification= annotationItem.identification.name + "\n" + annotationItem.identification.code
        pdf.add_annotation(
            'text',
            Location(x1= xStart, y1= yEnd, x2= xEnd, y2= yStart, page= annotationItem.page - 1),
            Appearance(fill= [0.1, 0.1, 0.1], stroke_width= 2, font_size= 8, content= textIdentification),
        )
    except Exception as e:
        #TODO print logging
        print(str(e))

# START APP
uvicorn.run(mainhandler,
            host="127.0.0.1",
            port=8000,
            reload=False)
