import pygame
import sys
from math import sqrt
import pickle
import glob

mosaicData = []

def getMapData(mosaicSet, pennySet):

    mosaicLow= 255
    mosaicHigh= 0
    pennyLow= 255
    pennyHigh= 0

    for i in mosaicSet:
        if i[1] < mosaicLow:
            mosaicLow = i[1]
        if i[1] > mosaicHigh:
            mosaicHigh = i[1]

    for i in pennySet:
        if i[0] < pennyLow:
            pennyLow = i[0]
        if i[0] > pennyHigh:
            pennyHigh = i[0]

    mosaicSpan = mosaicHigh - mosaicLow
    pennySpan = pennyHigh - pennyLow

    steps = pennySpan/float(mosaicSpan)

    return (steps, mosaicLow, pennyLow, pennyHigh)

def calcMapValue(value, MapData, pennySet):
    steps = MapData[0]
    mosaicLow = MapData[1]
    pennyLow = MapData[2]
    pennyHigh = MapData[3]

    increment = int((value-mosaicLow)*steps)
    return pennyLow+increment

##This dict is a hack for testing
valueSet = {35: 'sampleSet/000032-penny.png', 36: 'sampleSet/000033-penny.png', 43: 'sampleSet/000031-penny.png', 44: 'sampleSet/000012-penny.png', 45: 'sampleSet/000030-penny.png', 49: 'sampleSet/000029-penny.png', 50: 'sampleSet/000035-penny.png', 51: 'sampleSet/000018-penny.png', 54: 'sampleSet/000014-penny.png', 55: 'sampleSet/000011-penny.png', 57: 'sampleSet/000051-penny.png', 58: 'sampleSet/000017-penny.png', 59: 'sampleSet/000010-penny.png', 60: 'sampleSet/000034-penny.png', 62: 'sampleSet/000050-penny.png', 64: 'sampleSet/000054-penny.png', 65: 'sampleSet/000026-penny.png', 66: 'sampleSet/000028-penny.png', 68: 'sampleSet/000027-penny.png', 71: 'sampleSet/000057-penny.png', 72: 'sampleSet/000016-penny.png', 73: 'sampleSet/000038-penny.png', 74: 'sampleSet/000008-penny.png', 75: 'sampleSet/000040-penny.png', 77: 'sampleSet/000061-penny.png', 78: 'sampleSet/000060-penny.png', 79: 'sampleSet/000005-penny.png', 86: 'sampleSet/000042-penny.png', 89: 'sampleSet/000009-penny.png', 94: 'sampleSet/000022-penny.png', 97: 'sampleSet/000006-penny.png', 99: 'sampleSet/000049-penny.png', 100: 'sampleSet/000041-penny.png', 103: 'sampleSet/000046-penny.png', 106: 'sampleSet/000020-penny.png', 107: 'sampleSet/000058-penny.png', 109: 'sampleSet/000047-penny.png', 114: 'sampleSet/000024-penny.png', 115: 'sampleSet/000059-penny.png', 117: 'sampleSet/000043-penny.png', 126: 'sampleSet/000001-penny.png', 129: 'sampleSet/000021-penny.png', 134: 'sampleSet/000023-penny.png', 138: 'sampleSet/000056-penny.png', 148: 'sampleSet/000055-penny.png', 156: 'sampleSet/000045-penny.png'}
##end testing hack

#### Testruns: ####

# mahler2 runGame(786,976,8)
# mahler2-lowcontrast.jpg runGame(786,976,8)
# mahler2-cropped.jpg runGame(534,798,8)

def tm():
    from time import time
    for key in valueSet.keys():
        pixel = getPixelArray(valueSet[key])
        x = len(pixel)/2
        r = x
        if r%2 == 0:
            r -= 1
        y = getAllPointsInCircle(x,x,r)
        t0 = time()
        z= getCircleAverageLuminosity(pixel,y)
        t1 = time()
        print key,z,t1-t0

def getPixelLuminance(pixelColors):
    #pixelColors will be 3 value tuple

    #### Calculating Luminance ####
    #http://stackoverflow.com/a/689547
    # first divide R G B by 255, and compute
    # Y = .2126 * R^gamma + .7152 * G^gamma + .0722 * B^gamma
    # assume gamma of 2.2
    
    #actually ended up going with this simple equation:
    #http://stackoverflow.com/a/596243
    
    lum = (.299 * pixelColors[0]) + \
          (.587 * pixelColors[1]) + \
          (.114 * pixelColors[2])
    
    return int(lum)

###############################

#### Is point inside a circle? ####
#http://stackoverflow.com/a/15856549
#
# Quadratic equation calculates if it is on the hypotenuse
# Do this for one quadrant and then transpose the points

def getAllPointsInCircle(x,y,r):
    quarterPoints = []

    for testX in range(x-r,x+1):
        for testY in range(y-r,y+1):
            aLen = x-testX
            bLen = y-testY
            if (aLen**2) + (bLen**2) <= r*r:
                quarterPoints.append((testX,testY))
    
    #We now have a quarter circle, fill out the set
    allPoints = set([]) #use a set to avoid duplicate points
    for points in quarterPoints:
        
        reflectX = x+(x-points[0])
        reflectY = y+(y-points[1])

        allPoints.add(points)
        allPoints.add((reflectX,points[1]))
        allPoints.add((points[0],reflectY))
        allPoints.add((reflectX,reflectY))
    return allPoints


def testPoints(x):
    #Just a quick test to sanity check circle points set
    for i in range(21):
            thisRow = ""
            for j in range(21):
                    if (j,i) in x:
                            thisRow += "0 "
                    else:
                            thisRow += "- "
            print thisRow

###################################

def calcVertices(xSize,ySize,horizontalBisect,verticalDist):
    #returns points for equidistance circle centers in plane bound by x,y
    allVertices = []

    #starting vertices accounts for left and top padding
    curX = horizontalBisect
    curY = horizontalBisect
    row = 0

    while True:
        allVertices.append((curX,curY))
        #print allVertices[-1]
        #increment X
        curX += (2*horizontalBisect)

        #check for X overflow
        if curX > (xSize-horizontalBisect):
            row += 1
            curX = horizontalBisect+((row%2)*horizontalBisect)
            curY = curY + verticalDist
            if curY > (ySize-horizontalBisect):
                return allVertices

def getPixelArray(filename):
    #Get all RGB pixel colors from this image file
    try:
        image = pygame.image.load(filename)
    except pygame.error, message:
        print "Cannot load image:", filename
        raise SystemExit, message
    return pygame.surfarray.array3d(image)

def getLuminosityValues(listOfPoints, scalingValue, radiusBeforeScaling, sourceImage):
    #scaling value is how much to divide the
    #xy values by to fit within source image resolution
    lumList = []
    
    #Get pixel data from source image
    pixels = getPixelArray(sourceImage)
    #print pixels.shape

    adjustedR = radiusBeforeScaling/scalingValue
    testPoints = getAllPointsInCircle(adjustedR, adjustedR, adjustedR)

    #iterate each point in listOfPoints
    for point in listOfPoints:
        #get list of points in circle around each point
        testOffsetX = (point[0]/scalingValue)-adjustedR
        testOffsetY = (point[1]/scalingValue)-adjustedR

        lumAvg = getCircleAverageLuminosity( \
            pixels, \
            testPoints, \
            (testOffsetX, testOffsetY) \
            )
        lumList.append([point,lumAvg])
        if len(lumList)%250 == 0:
            print "Calculated",len(lumList),"values so far..."

    return lumList

def getCircleAverageLuminosity(pixArray, pixelsToTest, offsets=(0,0)):
    #pixArray is an image loaded and passed into this function
    #pixelsToTest are a circular area of points (x,y)
    #offsets are so you can use the same pixelsToTest array and move it around
    #a larger image if necessary.
    pixelAverages = [0,0,0]
    #moved to averaging colors then calculating luminance (~6.9x speedup).
    #possible loss of precision? But I think it is still valid. 
    for point in pixelsToTest:
        thisPixel = pixArray[point[0]+offsets[0], point[1]+offsets[1]]
        pixelAverages[0] += thisPixel[0]
        pixelAverages[1] += thisPixel[1]
        pixelAverages[2] += thisPixel[2]
    pixelAverages[0] = pixelAverages[0]/len(pixelsToTest)
    pixelAverages[1] = pixelAverages[1]/len(pixelsToTest)
    pixelAverages[2] = pixelAverages[2]/len(pixelsToTest)
    pixelLum = getPixelLuminance(pixelAverages)
    return pixelLum

def samplePennies(baseName = 'sampleSet/{number}-penny.png'):
    #process the penny sample set to characterize their luminance values
    #returns list of tuples: (luminance value, image name)

    #default image names look like: 'sampleSet/000001-penny.png'
    #images should be square with penning spanning edge to edge
    #this will automatically poll largest circular area in the image

    sampleFileList = glob.glob(baseName.format(number="*"))
    circlePointSets = []
    
    pennySet = {}
    for sample in sampleFileList:
        #assume sample is square, use height to get values we need
        img = pygame.image.load(sample)
        radius = img.get_height()/2
        if radius%2 == 0:
            radius -= 1
        lumValue = getLuminosityValues([(radius,radius)],1,radius,sample)[0][1]

        if lumValue not in pennySet.keys():
            pennySet[lumValue] = [sample]
        else:
            pennySet[lumValue].append(sample)
        #print pennySet[lumValue]
    return pennySet

def picklePennies():
    #sample all pennies and write output to a file for later use
    saveSet = samplePennies()
    with open("pennySet.p","wb") as outfile:
        pickle.dump(saveSet, outfile)

def unPicklePennies():
    #read in previously harvested sample set data
    with open("pennySet.p","rb") as infile:
        saveSet = pickle.load(infile)
    return saveSet

def runGame(sourceImage='mahler2-cropped.jpg',radius=32,scalingValue=8,usePennies=False):
    from time import time
    t0 = time()
    #Parameters:
    #sourceImage - Image you want to create as a penny mosaic
    #radius - radius in pixels of each penny area for this image
    #scalingValue - how much larger should the mock up be than the source image
    #393x488

    inputImage = pygame.image.load(sourceImage)

    pygameSurfaceX = inputImage.get_rect().size[0]*scalingValue
    pygameSurfaceY = inputImage.get_rect().size[1]*scalingValue

    #horizontal distances should be easy:
    horizontalBisect = radius

    #vertial is trickier (non-integer)
    verticalDist = int(sqrt(((horizontalBisect*2)**2)-(horizontalBisect**2)))

    #stock colors
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    darkBlue = (0,0,128)
    white = (255,255,255)
    black = (0,0,0)
    pink = (255,200,200)

    #Get a list of all points
    print "Generating penny locations"
    testPoints = calcVertices(pygameSurfaceX, \
                              pygameSurfaceY, \
                              horizontalBisect, \
                              verticalDist)

    #Get pixel data from source image
    print "Calculating luminance of penny areas"
    circlesAndLum = getLuminosityValues(testPoints, scalingValue, radius, sourceImage)
    global mosaicData
    mosaicData = circlesAndLum
    print "Total pennies for this mosaic:",len(circlesAndLum)

    #Show how it's going to look!
    pygame.init()
    screen = pygame.display.set_mode((pygameSurfaceX,pygameSurfaceY))
    screen.fill((187,136,85))
    
    if usePennies:
        pennyImages = unPicklePennies()
        
        #TODO: Normalize the spans of lightness

        #FIXME: this is faked, needs more thought
        for group in circlesAndLum:
            testLum = group[1]-65 #lum is group[1]
            loopFlag = True
            while loopFlag:
                #TODO: test statement to iterate to correct penny
                if testLum in valueSet.keys():
                    loopFlag = False
                else:
                    testLum += 1
                if testLum > 156:
                    testLum = 156
                    loopFlag = False
            
            
            img = pygame.image.load(valueSet[testLum])
            img = pygame.transform.scale(img, (radius*2, radius*2))
            screen.blit(img,(group[0][0]-radius,group[0][1]-radius))
    else:
        print "Using greyscale circles (parameter option)" 
        for group in circlesAndLum:
            pygame.draw.circle(screen, \
                               (group[1],group[1],group[1]), \
                               group[0],
                               horizontalBisect \
                               )
    
    
    print "Saving screenshot."
    t1 = time()
    print t1-t0
    pygame.image.save(screen, "screenshot.jpeg")
    pygame.display.update()
    
    loopFlag = True
    while loopFlag:
       for event in pygame.event.get():
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                 loopFlag = False

    pygame.quit()
    #return circlesAndLum
