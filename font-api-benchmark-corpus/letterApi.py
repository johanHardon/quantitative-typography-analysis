import argparse
import requests
import cv2
import numpy as np
import os

parser = argparse.ArgumentParser()
parser.add_argument("-f", type=str, required=True, help="(Required) Add a string with the family name, use flag: -f")
parser.add_argument("-s", type=str, required=True, help="(Required) Add a string with unique style name, use flag_ -s")
parser.add_argument("-c", type=str, required=True, help="(Required) Add a string with category, use flag_ -c")
parser.add_argument("-l", type=str, required=True, help="(Required) Add a string with a letter(s), use flag: -l")
args = parser.parse_args()
FAMILY_NAME = args.f
STYLE_NAME = args.s
CATEGORY = args.c
LETTER = args.l

def fetchImage():
    styleId = 0
    print("FamilyName", FAMILY_NAME.replace(" ", "%20"))
    try:
        apiResponse = requests.get(f'https://api.myfonts.net/v1/family?api_key=EE5HsjFDom5yIcGTdBu2KhMBO&name={FAMILY_NAME.replace(" ", "%20")}&extra_data=styles|default_style_id')
        if apiResponse.json()["total_results"] == 0:
            print(f'There was an error while fetching {FAMILY_NAME.replace(" ", "%20")}. Check your -f string')
        else:
            familyResponseJson = apiResponse.json()["results"]
            styleKeys = list(familyResponseJson.keys())                  
            for s in range(len(styleKeys)):
                if "styles" in familyResponseJson[styleKeys[s]]:
                    styleResponseJson =familyResponseJson[styleKeys[s]]['styles']                     
                    for j in range(len(styleResponseJson)):
                        styleNameApi = styleResponseJson[j]["name"]
                        if styleNameApi.casefold() == STYLE_NAME.casefold():
                            styleId = styleResponseJson[j]["id"]                        
            if styleId == 0: 
                styleId = int(apiResponse.json()["results"][styleKeys[s]]["DefaultStyleID"])
                print(f'Used default styleid for style name: {STYLE_NAME}')            
            imageResponse = requests.get(f'https://apicdn.myfonts.net/v1/fontsample?id={styleId}&text={LETTER}&size=250' , stream=True).raw
            image = np.asarray(bytearray(imageResponse.read()), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            resultPath = f'image-result/{CATEGORY.replace(" ","_")}/{FAMILY_NAME.replace(" ", "-")}/'
            if os.path.isdir(resultPath) is False:
               os.makedirs(resultPath) 
            cv2.imwrite(resultPath +f'{STYLE_NAME.replace(" ", "-")}-{LETTER}.png', image)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)    
fetchImage()
