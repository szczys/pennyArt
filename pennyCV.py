# Citations for this code:
# http://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/
# 
from PIL import Image, ImageOps, ImageDraw
import numpy as np
import cv2
import glob

SAMPLEBASENAME = 'sampleSet/{number}-penny.png'
PENNYSAMPLEWIDTH = 200

#infile = "reduced.jpg"
#infile = "/home/mike/Desktop/pennySample.pnm"
infile = "/home/mike/Desktop/gscan-sample.jpg"

circles = []
postViewing = Image.open(infile)

def genAndSavePennySamples():
    findPennies()
    nextFilename = getNextSampleFilename();
    for p in range(len(circles)):
        savePenny(p, nextFilename)
        nextFilename = incrementFilename(nextFilename)
    

def findPennies():
    global circles
    image = cv2.imread(infile)

    output = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 2.6, 200, minRadius=105, maxRadius=118)



    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")

        for (x, y, r) in circles:
            cv2.circle(output, (x,y), r, (0,255,0), 4)
        '''
        #This commented out block will display the circle detection but it's going to freeze your program so use only for debugging
        cv2.imshow('ImageWindow',np.hstack([image, output]))
        cv2.waitKey(2000) #& 0xFF #The bitwise and is a hack for 64-bit machines
        '''

def savePenny(num, fn):
    if len(circles) == 0:
        print "No pennies in the circles array."
        return
    x,y,r = circles[num]
    crop_rectangle = (x-r,y-r, x+r,y+r)
    cropped_im = postViewing.crop(crop_rectangle)

    mask = makeCircleMask(r)
    transparent = ImageOps.fit(cropped_im, mask.size, centering=(0.5, 0.5))
    transparent.putalpha(mask)
    #transparent.save('test.png')
    scaled = transparent.resize((PENNYSAMPLEWIDTH, PENNYSAMPLEWIDTH))
    scaled.save(fn)

def makeCircleMask(radius):
    #Tricks to make everything but penny transparent using mask:
    #http://stackoverflow.com/a/890114
    size = (radius*2,radius*2)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0,0)+size, fill=255)
    return mask

def getFileNumIdx():
    premask = SAMPLEBASENAME.format(number="######")
    fileNumIdx = len(premask.split("######")[0])
    return fileNumIdx

def getNextSampleFilename():
    #This will be called once and will find the highest
    #existing sample number and increment it by 1.
    #It will work even if there are some samples missing
    query = glob.glob(SAMPLEBASENAME.format(number="*"))
    if query == []:
        return SAMPLEBASENAME.format(number="000001")
    else:
        fileNumIdx = getFileNumIdx()
        highest = 0
        for fn in query:
            testVal = int(fn[fileNumIdx:fileNumIdx+6])
            if  testVal > highest:
                highest = testVal
        return makeSampleFilename(highest+1)

def makeSampleFilename(num):
    nextNum = str(num)
    nextNum = '0'*(6-len(nextNum)) + nextNum
    return SAMPLEBASENAME.format(number=nextNum)

def incrementFilename(curFn):
    fileNumIdx = getFileNumIdx()
    highest = int(curFn[fileNumIdx:fileNumIdx+6])+1
    return makeSampleFilename(highest)
