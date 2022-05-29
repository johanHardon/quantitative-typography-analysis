from importlib.resources import path
from unicodedata import category
import cv2
import argparse
import numpy as np
import csv

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", nargs='+', help="Input array of file path - file must be .png or .jpg and depict one letter")
parser.add_argument("-o", "--output", help="Path to output file. File must be .csv")
args = parser.parse_args()

def getConnectivity(contours):
    numberOfContours = len(contours)
    print(numberOfContours)
    if numberOfContours > 1:
        numberOfContours = 0        
    return numberOfContours

def getDetails(inputString):
    inputArr = inputString.split('/')
    category = "".join(inputArr[-5]).replace("-", " ")
    family= "".join(inputArr[-4]).replace("-", " ")
    style = "".join(inputArr[-3]).replace("-", " ")
    return family, style, category
    
def writeToCSV(category,family, style, connection):
    f = open(args.output, 'a', encoding='UTF8')
    writer = csv.writer(f, delimiter=';')
    row = [category, family,style, connection]
    writer.writerow(row)
    f.close()

connections = 0
pathArray = args.input
for i in range(len(pathArray)):
    image = cv2.imread(pathArray[i])
    height, width = image.shape[:2]
    print("height", height, "width", width)
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(grayImage, 230, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, contours, -1, (0,255,0), 1)
    connections += getConnectivity(contours)
family, style, category = getDetails(pathArray[i])  
if height == 13 and width == 120:
    connections = "-"
    print("No sample available for:", style)      
writeToCSV(category,family,style,connections)






