import argparse
import requests
import cv2
import numpy as np
import os

parser = argparse.ArgumentParser()
parser.add_argument("-f", type=str, required=True, help="(Required) Add a string with the family name, use flag: -f")
parser.add_argument("-s", type=str, required=True, help="(Required) Add a string with unique style name, use flag_ -s")
parser.add_argument("-i", type=str, required=True, help="(Required) Add a string with styleid, use flag_ -i")
parser.add_argument("-c", type=str, required=True, help="(Required) Add a string with category, use flag_ -c")
parser.add_argument("-l", type=str, required=True, help="(Required) Add a string with a letter(s), use flag: -l")
args = parser.parse_args()
FAMILY_NAME = args.f
STYLE_NAME = args.s
STYLE_ID = args.i
CATEGORY = args.c
LETTER = args.l

def makePathAndWriteImage(imageResponse, letter, specialFolder):
    image = np.asarray(bytearray(imageResponse.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    resultPath = f'database/{CATEGORY.replace(" ", "-")}/{FAMILY_NAME.replace(" ", "-")}/{STYLE_NAME.replace(" ", "-")}/{specialFolder}/'
    if os.path.isdir(resultPath) is False:
        os.makedirs(resultPath) 
    cv2.imwrite(resultPath+f'{STYLE_NAME.replace(" ", "-")}-{letter}.png', image)

def fetchImages():
    try:
        requestLetters = LETTER.split()
        print("running")
        print(STYLE_NAME)
        for letter in requestLetters:              
            if len(letter) == 1:
                imageResponse = requests.get(f'https://apicdn.myfonts.net/v1/fontsample?id={STYLE_ID}&text={letter}&size=250' , stream=True).raw
                makePathAndWriteImage(imageResponse, letter, specialFolder="one-letter")
            elif len(letter) == 2:
                imageResponse = requests.get(f'https://apicdn.myfonts.net/v1/fontsample?id={STYLE_ID}&text={letter}&size=200' , stream=True).raw
                makePathAndWriteImage(imageResponse, letter, specialFolder="two-letter")
            else:
                imageResponse = requests.get(f'https://apicdn.myfonts.net/v1/fontsample?id={STYLE_ID}&text={letter}&size=92' , stream=True).raw
                makePathAndWriteImage(imageResponse, letter, specialFolder="six-letter")
        print("..")
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err, STYLE_NAME)    
fetchImages()
