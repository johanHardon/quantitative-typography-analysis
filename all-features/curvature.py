import numpy as np
from random import randrange
import numpy.linalg as la
import cv2
import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Input file path")                # input img file path
parser.add_argument("-o", "--output", help="Output .csv file path")         # output csv file path
parser.add_argument("-t1", "--maxcorner1", help="Threshold corners")        # Threshold val for corners
parser.add_argument("-t2", "--drawstraight", help="Threshold straights")    # Threshold val for straight line detection
parser.add_argument("-t3", "--maxcorner2", help="Threshold curve")          # Threshold val curve sensitivity
parser.add_argument("-s", "--removestraight", help="Threshold straights")   # Threshold val for removing straight line points
args = parser.parse_args()
np.seterr(divide='ignore', invalid='ignore') 


def rel_thresh(img, threshval):
    return float(threshval) * (img.size / 94221)    # Calculate threshold value relative to pixel count

# Calc angle from three points
def get_angle(p1, p2, p3):
    v1 = np.subtract(p2, p1)
    v2 = np.subtract(p2, p3)
    cos = np.inner(v1, v2) / la.norm(v1) / la.norm(v2)
    rad = np.arccos(np.clip(cos, -1.0, 1.0))
    return np.rad2deg(rad)

# Get angles for all points in p
def get_angles(p, d):
    n = len(p)
    return [(p[i], get_angle(p[(i-d) % n], p[i], p[(i+d) % n])) for i in range(n)]


def remove_straight(p):
    angles = get_angles(p, 2)   # approximate angles at points
    return [p for (p, a) in angles if a < int(args.removestraight)]    # remove points with almost straight angles (original 170)


def draw_straights(img, pts, thresh):
        angles = get_angles(pts, 1)
        j=0
        straights = 0
        while j < len(angles):
            k = (j + 1) % len(angles)
            (pj, aj) = angles[j]
            (pk, ak) = angles[k]
            dist = la.norm(np.subtract(pj,k))

            if aj < 125 and ak < 125 and dist >= thresh/2: #if both points are angles
                cv2.line(img, pj, pk, (randrange(255), randrange(255), randrange(255)), 1)
                straights += 1

            elif (la.norm(np.subtract(pj, pk)) >= thresh): #If the distance between pj, pk >= threshold
                cv2.line(img, pj, pk, (0, 255, 0), 1)
                straights += 1
        
            j += 1
        return straights

def max_corner(p, thresh):
    angles = get_angles(p, 1)           # get angles at points
    j = 0

    while j < len(angles):              # for each point
        k = (j + 1) % len(angles)       # and its successor
        (pj, aj) = angles[j]
        (pk, ak) = angles[k]

        if la.norm(np.subtract(pj, pk)) <= thresh:      # if points are close
            if aj > ak:                                 # remove point with greater angle
                angles.pop(j)
            else:
                angles.pop(k)
        else:
            j += 1
    return [p for (p, a) in angles]

def print_count(name, regions, angles, curves, straights): # counts to std.out
    print(f"""{name}
            Regions: {regions}
            Angles: {angles}
            Curves: {curves}
            Straights: {straights}\n""")

def write_to_csv(img, category, family, style, glyph, regions, straights, angles, curves):
    f = open(args.output, 'a', encoding='UTF8')
    writer = csv.writer(f, delimiter=';')
    row = []
    if img.shape == (33, 140, 3):    
        print(family)
        print(img.shape)

        row = [category, family, style, glyph, '-', '-', '-', '-']
    else:
        row = [category,family,style, glyph, regions, straights, angles, curves]
    writer.writerow(row)
    f.close()

def calc_relative_thresh(n):
    return int((n / img.size) * 100)

def main():
    img = cv2.imread(args.input)
    img = cv2.copyMakeBorder(img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, None, (255, 255, 255))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY_INV)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    anglesCount = 0
    curvesCount = 0
    straightsCount = 0
    cc = 0
    curvesList = []
    for c in contours:                  # for each contour
        cc += 1
        pts = [v[0] for v in c]         # get pts from contour
        pts = remove_straight(pts)      # remove almost straight angles
        pts = max_corner(pts, rel_thresh(img, args.maxcorner1))        # remove nearby points with greater angle
        angles = get_angles(pts, 1)     # get angles at points

        for (p, a) in angles:           # for each entry in angles
            if a < 125:                 # if angle of a point is < 125
                anglesCount += 1        # it is a corner. Inc anglesCount and draw point.
                cv2.circle(img, p, 3, (0, 0, 255), -1)
            else:
                curvesList.append(p)    # Else, append point and angle to a list of curve tuples.
        
        curvesList = max_corner(curvesList, rel_thresh(img, args.maxcorner2)) # Remove nearby curve points
        straightsCount +=  draw_straights(img, pts, rel_thresh(img, args.drawstraight)) # points with dist >= thresh are ends of straight line. Count occurences of straights, draw them and return the count.

        

    for p in curvesList:
            curvesCount += 1            # Count number of curves and draw a point for each
            cv2.circle(img, p, 3, (255, 0, 0), -1)


    
    path = args.input
    inputArr = path.split('/')
    family = "".join(inputArr[-4]).replace("-", " ") 
    category = "".join(inputArr[-5]).replace("-", " ")
    style = "".join(inputArr[-3]).replace("-", " ")
    glyph = "".join(inputArr[-1][-5])
    print_count(style, len(contours), anglesCount, curvesCount, straightsCount)
    write_to_csv(img, category, family, style, glyph, len(contours), straightsCount, anglesCount, curvesCount) 
    cv2.destroyAllWindows()

main()
