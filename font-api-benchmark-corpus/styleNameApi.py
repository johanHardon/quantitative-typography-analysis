import os
import sys
import cv2
import requests
import numpy as np
import csv
from collections import defaultdict


CSV_FILE = sys.argv[1]
fontDict = defaultdict(list)
def extractData():
    with open(CSV_FILE,'r', encoding='latin-1')as file:
        filecontent=csv.reader(file, delimiter=';')
        for row in filecontent:
            if row[0] !="Family":                
                if len(fontDict[row[0].replace(" ", "-")]) == 0:
                    fontDict[row[0].replace(" ", "-")].append(row[1])
                    fontDict[row[0].replace(" ", "-")].append(row[2])
                    newPath = f'image-results/{row[2]}/{row[0].replace(" ", "-")}/'
                    if os.path.isdir(newPath) is False:
                        os.makedirs(newPath) 

def fetchImages():
    print("Number of fonts left to be fetched:")
    fontCounter = len(fontDict)
    for i in range(len(fontDict)):
        styleId = 0
        try:
            requestString = str(list(fontDict.keys())[i].replace("-", "%20"))
            apiResponse = requests.get(f'https://api.myfonts.net/v1/family?api_key=EE5HsjFDom5yIcGTdBu2KhMBO&name={requestString}&extra_data=styles|default_style_id')
            if apiResponse.json()["total_results"] == 0:
                print(f"There was an error while fetching {list(fontDict.keys())[i]}. Check line {str(i+2)} in the csv file for correct input")
            else:
                familyResponseJson = apiResponse.json()["results"]
                styleKeys = list(familyResponseJson.keys())                          
                for s in range(len(styleKeys)):
                    styleResponseJson =familyResponseJson[styleKeys[s]]["styles"]              
                    typefaceKey =list(fontDict.keys())[i]                
                    uniqueStyleName = fontDict[typefaceKey][0]                
                    for j in range(len(styleResponseJson)):
                        styleNameApi = styleResponseJson[j]["name"]
                        if styleNameApi == uniqueStyleName:
                            styleId = styleResponseJson[j]["id"]
                if styleId == 0: 
                    styleId = int(apiResponse.json()["results"][styleKeys[s]]["DefaultStyleID"])
                    print(f'Used default styleid for typeface: {str(list(fontDict.keys())[i]).replace("-", " ")}')
                for j in range(6):
                    letters = ['H','p','k','x','o','a']
                    fontType = fontDict[typefaceKey][1]
                    folderName = list(fontDict.keys())[i]
                    fileName = list(fontDict.keys())[i] +"-" + letters[j] + ".png"
                    fontResponse = requests.get(f'https://apicdn.myfonts.net/v1/fontsample?id={styleId}&text={letters[j]}&size=250' , stream=True).raw
                    img = np.asarray(bytearray(fontResponse.read()), dtype="uint8")
                    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
                    resultPath = f'image-results/{fontType}/{folderName}/{fileName}'
                    cv2.imwrite(resultPath, img)
        except:
            print(f"An error occured while fetching following typeface: {str(list(fontDict.keys())[i])}")
        print(fontCounter)
        fontCounter -= 1
          
extractData()  
fetchImages()