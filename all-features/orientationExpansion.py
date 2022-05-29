from click import style
import cv2
import numpy as np
import argparse
import csv

#Define CL flags and store in args
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Input file path - file must be .png or .jpg and depict one letter")
parser.add_argument("-o", "--output", help="Path to output file. File must be .csv")
args = parser.parse_args()

#Draws a rectangle trimmed to the outer contour on the original image
#Can easily be trimmed to also crop the image
def drawOuterContour(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    nonz = cv2.findNonZero(threshed)

    x,y,w,h = cv2.boundingRect(nonz)
    cropped = gray[y:y+h, x:x+w] #For cropping the img around the border instead of drawing on the original img
    cv2.rectangle(img, (x, y), (x+w, y+h), (0,0,255),1) 
    
    return cropped, h, w

#Write output to CSV
def writeToCSV(category, family, style, glyph, h, w):
    f = open(args.output, 'a', encoding='UTF8')
    writer = csv.writer(f, delimiter=';')
    row = [category,family, style, glyph, h, w]
    writer.writerow(row)
    f.close()

#Extract category, family, styleName and glyph from input string
def getDetails(inputString):
    inputArr = inputString.split('/')
    family = "".join(inputArr[-4]).replace("-"," ")
    category = "".join(inputArr[-5]).replace("-"," ")
    style = "".join(inputArr[-3]).replace("-"," ")
    glyph = inputArr[-1][-5]
    return category, family, style, glyph

img = cv2.imread(args.input)
img, h, w = drawOuterContour(img)
category, family, style, glyph = getDetails(args.input)
#Sets conditional for images with no sample available before writing to csv
if h == 13 and w == 120:
    h = "-"
    w = "-"
    print("no sample available for: ", style)
writeToCSV(category, family, style, glyph, h, w)