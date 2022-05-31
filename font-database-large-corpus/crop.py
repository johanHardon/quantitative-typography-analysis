import cv2
import numpy as np
import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Input file path - file must be .png or .jpg and depict one letter")
args = parser.parse_args()

#Draws a rectangle trimmed to the outer contour on the original image
#Can easily be trimmed to also crop the image
def drawOuterContour(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    nonz = cv2.findNonZero(threshed)
    x,y,w,h = cv2.boundingRect(nonz)
    cropped = gray[y:y+h, x:x+w] #For cropping the img around the border instead of drawing on the original img
    #cv2.rectangle(img, (x, y), (x+w, y+h), (0,0,255),1)     
    return cropped, h, w

#Extract family and glyph from input string
def getDetails(inputString):
    inputArr = inputString.split('/')
    parentFolder = inputArr[0]
    category = inputArr[1]
    family = inputArr[2]
    styleName = inputArr[3]
    specialFolder = inputArr[4]
    glyph = inputArr[5]
    return parentFolder, family, styleName, glyph, category, specialFolder

img = cv2.imread(args.input)
img, h, w = drawOuterContour(img)
parentFolder, family, styleName, glyph, category, specialFolder = getDetails(args.input)
resultPath = f'{parentFolder}/{category}/{family}/{styleName}/{specialFolder}/'
print("Running" + resultPath)
cv2.imwrite("./"+resultPath +f'{glyph}', img)


