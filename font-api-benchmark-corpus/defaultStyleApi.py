import os
import cv2
import requests
import numpy as np
import csv
import sys

CSV_FILE = sys.argv[1]
extractedFonts = []
extractedCategories = []
requestsStrings = []

 
def extractFileContent():
    global extractedFonts
    global extractedCategories
    global requestsStrings
    with open(CSV_FILE,'r', encoding='utf-8-sig') as file:
        filecontent=csv.reader(file, delimiter=';')    
        for row in filecontent:
            if row[0] != "Type":  
                extractedFonts.append(row[1])
                extractedCategories.append(row[0])
                requestsStrings.append(row[1])

                newPath = f'image-results/{row[0]}/{row[1].replace(" ", "-")}/'
                if os.path.isdir(newPath) is False:
                    os.makedirs(newPath)
                    print("her er jeg")
        extractedFonts = [e.replace(" ", "-") for e in extractedFonts]
        requestsStrings = [e.replace(" ", "%20") for e in requestsStrings]
        print(extractedFonts)


def fetchFontImages():
    extractFileContent()
    fontCounter = len(requestsStrings)
    print("Number of fonts left to be fetched:")  

#for i in range(len(requestsStrings)):
    i = 0
    try:
        for j in range(7):
            apiResponse = requests.get(f'https://api.myfonts.net/v1/family?api_key=EE5HsjFDom5yIcGTdBu2KhMBO&name={requestsStrings[i]}&extra_data=styles|default_style_id')
            if apiResponse.json()["total_results"] == 0:
                print(f"There was an error while fetching {extractedFonts[i]}. Check line {str(i+2)} in the csv file for correct input")
                break
            else:
                result = apiResponse.json()["results"]            
                idOfFont = list(result.keys())[0]
                defaultStyleId = result[idOfFont]["DefaultStyleID"]
                requestedLetters = ['H','p','k','x','o','a','Hpkxoa']
                fileName = extractedFonts[i] +"-" + requestedLetters[j] + ".png"
                imageResponse = requests.get(f'https://apicdn.myfonts.net/v1/fontsample?id={defaultStyleId}&text={requestedLetters[j]}&size=300' , stream=True).raw
                image = np.asarray(bytearray(imageResponse.read()), dtype="uint8")
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)
                resultPath = f'image-results_300/{extractedCategories[i]}/{extractedFonts[i]}/{fileName}'
                cv2.imwrite(resultPath, image)
        fontCounter -= 1
    except:
        print(apiResponse.json())        
    print(str(fontCounter)) 



fetchFontImages()
