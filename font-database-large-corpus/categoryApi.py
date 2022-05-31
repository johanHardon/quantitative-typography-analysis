import argparse
from unicodedata import category
import requests
import cv2
import numpy as np
import os
import csv

parser = argparse.ArgumentParser()
parser.add_argument("-c", type=str, required=True, help="(Required) Add a string with category, use flag_ -c")
parser.add_argument("-o", type=str, required=True, help="(Required) Add a string with the path to a csv file, use flag: -0")
args = parser.parse_args()
CATEGORY = args.c
OUTPUTFILE = args.o

def writeToCSV(category, typeface, styleName, styleId):
    f = open(OUTPUTFILE, 'a', encoding='UTF8')
    writer = csv.writer(f, delimiter=';')
    row = [category, typeface, styleName, styleId]
    writer.writerow(row)
    f.close()

def fetchStyles():
    try:
        apiResponse = requests.get(f'https://api.myfonts.net/v1/family?api_key=EE5HsjFDom5yIcGTdBu2KhMBO&&category={CATEGORY}&extra_data=styles')
        if apiResponse.json()["total_results"] == 0:
            print(f'There was an error while fetching {CATEGORY}. Check your -c string')
        else:
            familyResponseJson = apiResponse.json()["results"]            
            familyKeys = list(familyResponseJson.keys())                              
            for s in range(len(familyKeys)):
                if "styles" in familyResponseJson[familyKeys[s]]:
                    styleResponseJson =familyResponseJson[familyKeys[s]]['styles']                     
                    for j in range(len(styleResponseJson)):
                        styleName = styleResponseJson[j]["name"]
                        styleId = styleResponseJson[j]["id"]
                        familyName = familyResponseJson[familyKeys[s]]["name"].replace("&trade;", u"\u2122").replace("&reg;",u"\xae")
                        writeToCSV(CATEGORY.replace("-"," "), familyName,styleName, styleId)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)    
fetchStyles()
