from curses import raw
from multiprocessing.sharedctypes import Value
import os
import cv2
import requests
import numpy as np
import csv
from collections import defaultdict
import json

# 
#extractedTypefaces = []
extractedTypes = []
requestsStrings = []
fontDict = defaultdict(list)
def extractData():
    global requestsStrings
    with open('typography_data.csv','r')as file:
        filecontent=csv.reader(file, delimiter=';')
        for row in filecontent:
            if row[0] !="Collection":
                #extractedTypefaces.append(row[1])
                extractedTypes.append(row[3])
                requestsStrings.append(row[1])
                if len(fontDict[row[1].replace(" ", "-")]) == 0:
                    fontDict[row[1].replace(" ", "-")].append(row[2])
                    fontDict[row[1].replace(" ", "-")].append(row[3])

                    newPath = f'image-result/{row[3]}/{row[1].replace(" ", "-")}/'
                    if os.path.isdir(newPath) is False:
                        os.makedirs(newPath)
    #extractedTypefaces = [e.replace(" ", "-") for e in extractedTypefaces]
    requestsStrings = [e.replace(" ", "%20") for e in requestsStrings]

    
    print("Number of fonts left to be fetched:")
def getImages():
    extractData()
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
                for t in range(len(list(familyResponseJson.keys()))):
                    styleKeys = list(familyResponseJson.keys())
                    styleResponseJson =familyResponseJson[styleKeys[t]]["styles"]
                    
                    # styleResponseSeperate = familyResponseJson[styleResponseJson]["styles"]
                    
                    typefaceKey =list(fontDict.keys())[i]
                    subString = fontDict[typefaceKey][1]# + " " + fontDict[typefaceKey][0]
                    for j in range(len(styleResponseJson)):
                        fullString = styleResponseJson[j]["name"]
                        if fullString.find(subString) != -1:
                            styleId = styleResponseJson[j]["id"]
                    if styleId == 0: 
                        styleId = int(apiResponse.json()["results"][styleKeys[0]]["DefaultStyleID"])
                print("styleId: " + str(styleId))
                for j in range(7):
                    letters = ['H','p','k','x','o','a','Hpkxoa']
                    fontType = fontDict[typefaceKey][1]
                    folderName = list(fontDict.keys())[i]
                    fileName = list(fontDict.keys())[i] +"-" + letters[j] + ".png"
                    fontResponse = requests.get(f'https://apicdn.myfonts.net/v1/fontsample?id={styleId}&text={letters[j]}&size=100' , stream=True).raw
                    img = np.asarray(bytearray(fontResponse.read()), dtype="uint8")
                    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
                    resultPath = f'image-result/{fontType}/{folderName}/{fileName}'
                    cv2.imwrite(resultPath, img)
        except:
            print(f"An error occured while fetching following typeface: {str(list(fontDict.keys())[i])}")
        print(fontCounter)
        fontCounter -= 1    


getImages()   
    
    
    
    # fontCounter = len(requestsStrings)
    # print("Number of fonts left to be fetched:")  
#for i in range(len(requestsStrings)):
    # i = 0
    # try:
        # for j in range(7):
            # apiResponse = requests.get(f'https://api.myfonts.net/v1/family?api_key=EE5HsjFDom5yIcGTdBu2KhMBO&name={requestsStrings[i]}&extra_data=styles|default_style_id')
            # if apiResponse.json()["total_results"] == 0:
                # print(f"There was an error while fetching {extractedFonts[i]}. Check line {str(i+2)} in the csv file for correct input")
                # break
            # else:
                # result = apiResponse.json()["results"]            
                # idOfFont = list(result.keys())[0]
                # defaultStyleId = result[idOfFont]["DefaultStyleID"]
                # requestedLetters = ['H','p','k','x','o','a','Hpkxoa']
                # fileName = extractedFonts[i] +"-" + requestedLetters[j] + ".png"
                # imageResponse = requests.get(f'https://apicdn.myfonts.net/v1/fontsample?id={defaultStyleId}&text={requestedLetters[j]}&size=100&behaviour=resize' , stream=True).raw
                # image = np.asarray(bytearray(imageResponse.read()), dtype="uint8")
                # image = cv2.imdecode(image, cv2.IMREAD_COLOR)
                # resultPath = f'image-results/{extractedCategories[i]}/{extractedFonts[i]}/{fileName}'
                # cv2.imwrite(resultPath, image)
        # fontCounter -= 1
    # except:
        # print(apiResponse.json())        
    # print(str(fontCounter)) 









