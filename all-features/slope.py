import cv2
import numpy as np
import argparse
import csv

#Input argument handling
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Input file path")
parser.add_argument("-o", "--output", help="Output file path")
args = parser.parse_args()

# find details for the specific fontstyle
PATH = args.input
PATHARRAY = PATH.split("/")
CATEGORY = "".join(PATHARRAY[-5]).replace("-", " ")
FAMILY = "".join(PATHARRAY[-4]).replace("-", " ")
STYLENAME = "".join(PATHARRAY[-3]).replace("-", " ")

#read in image
img = cv2.imread(PATH)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
edges = cv2.Canny(blurred, 50, 150, apertureSize=3)

def writeToCSV(category, family, styleName, slope):
    f = open(args.output, 'a', encoding='UTF8')
    writer = csv.writer(f, delimiter=';')
    row = [category, family, styleName, slope]
    writer.writerow(row)
    f.close()

def writeFile(path, file):
    cv2.imwrite(path, file)

def regionOfInterest(img):
	rows = (img.shape[0])
	cols = int(img.shape[1] * 0.5)
	return img[0:rows, 0:cols]


def findLineWithSmallestAngle(lines):
    if lines is not None:
        currentSmallest = lines[0]
        for line in lines:
            if line[0][1] < currentSmallest[0][1]:
                currentSmallest = line
        return currentSmallest
    return None

def drawHoughLine(line, img):
    if line is not None:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        #x1 stores the rounded off value of (r * cos(theta) - 1000 * sin(theta))
        x1 = int(x0 + 1000 * (-b))
        #y1 stores the rounded off value of (r * sin(theta) + 1000 * cos(theta))
        y1 = int(y0 + 1000 * (a))
        #x2 stores the rounded off value of (r * cos(theta) + 1000 * sin(theta))
        x2 = int(x0 - 1000 * (-b))
        #y2 stores the rounded off value of (r * sin(theta) - 1000 * cos(theta))
        y2 = int(y0 - 1000 * (a))

        cv2.line(img, (x1, y1), (x2, y2), (0,255,0), 2)
        angleInDegrees = np.degrees(line[0][1]) + 90
        writeToCSV(CATEGORY, FAMILY, STYLENAME, angleInDegrees)
    else:
        print(f"ERROR: {STYLENAME}")
        writeToCSV(CATEGORY, FAMILY, STYLENAME, '-')
print("running...", STYLENAME)
ROI = regionOfInterest(edges)
lines = cv2.HoughLines(ROI, 1, np.pi / 180, 65)
line = findLineWithSmallestAngle(lines)
drawHoughLine(line, img)

