import cv2
import numpy as np
import requests
import os

#Draws a rectangle trimmed to the outer contour on the original image
#Can easily be trimmed to also crop the image
def drawOuterContour(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 195, 255, cv2.THRESH_BINARY_INV)
    nonz = cv2.findNonZero(threshed)

    x,y,w,h = cv2.boundingRect(nonz)
    cropped = gray[y:y+h, x:x+w] #For cropping the img around the border instead of drawing on the original img
    print(f'Height: {h}, Width: {w}')

    
    #cv2.rectangle(img, (x, y), (x+w, y+h), (0,0,255),1) 
    #return img
    return cropped
#img = cv2.imread("begum.png")
#img = drawOuterContour(img)
#cv2.imshow("", img)
#cv2.waitKey(0)

path = "assets/"
directory = os.fsencode(path)
for file in os.listdir(directory):
    filename = path + os.fsdecode(file)  
    if filename.endswith(".png"):
        img = cv2.imread(filename )
        img = drawOuterContour(img) 
        
        outPath = "result_all/"
        cv2.imwrite(os.path.join(outPath, os.fsdecode(file)), img)

