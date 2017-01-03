import pygame
import sys
from math import sqrt
import pickle

#### Testruns: ####

# mahler2 runGame(786,976,8)
# mahler2-lowcontrast.jpg runGame(786,976,8)
# mahler2-cropped.jpg runGame(534,798,8)

def luminance(pixelColors):
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

    #iterate each point in listOfPoints
    for point in listOfPoints:
        #get list of points in circle around each point
        thisCirclePoints = getAllPointsInCircle(point[0]/scalingValue, \
                             point[1]/scalingValue, \
                             radiusBeforeScaling/scalingValue \
                             )
        lumSum = 0
        for circlePoint in thisCirclePoints:
            lumSum += luminance(pixels[circlePoint[0]][circlePoint[1]])
        lumAvg = lumSum/len(thisCirclePoints)
        #print point,lumAvg
        lumList.append([point,lumAvg])
        
    ##(utilize scaling to match source resolution)
    #Calculate average luminosity of all harvested points
    #associate this value with the xy inputs
    
    return lumList

def samplePennies(baseName = 'sampleSet/{number}-penny.png',imgDiameter=324,sampleCount=61):
    #process the penny sample set to characterize their luminance values
    #returns list of tuples: (luminance value, image name)

    #default image names look like: 'sampleSet/0001-penny.png'
    #images should be square with penning spanning edge to edge
    #this will automatically poll largest circular area in the image

    radius = imgDiameter/2 
    if radius%2 == 0:
        radius -= 1
    
    pennySet = []
    for i in range(1,sampleCount+1):
        #Normalize the number for the filename
        thisNum = str(i)
        thisNum = '0'*(4-len(thisNum)) + thisNum
        imgName = baseName.format(number=thisNum)
        lumValue = getLuminosityValues([(radius,radius)],1,radius,imgName)[0][1]
        pennySet.append((lumValue,imgName))
        print pennySet[-1]
    return pennySet

def picklePennies():
    #sample all pennies and write output to a file for later use
    saveSet = samplePennies()
    pickle.dump( saveSet, open( "pennySet.p", "wb" ) )
    

def runGame(sizeX,sizeY,radius):
    #393x488
    pygameSurfaceX = sizeX
    pygameSurfaceY = sizeY

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

    pygame.init()
    screen = pygame.display.set_mode((pygameSurfaceX,pygameSurfaceY))
    screen.fill(red)

    #Get a list of all points
    testPoints = calcVertices(pygameSurfaceX, \
                              pygameSurfaceY, \
                              horizontalBisect, \
                              verticalDist)

    #Get pixel data from source image
    #circlesAndLum = getLuminosityValues(testPoints, 2, radius, 'mahler2.jpg')
    #circlesAndLum = getLuminosityValues(testPoints, 2, radius, 'mahler2-lowcontrast.jpg')
    circlesAndLum = getLuminosityValues(testPoints, 2, radius, 'mahler2-cropped.jpg')
    
    print len(circlesAndLum)
    for group in circlesAndLum:
        pygame.draw.circle(screen, \
                           (group[1],group[1],group[1]), \
                           group[0],
                           horizontalBisect \
                           )

    #pygame.draw.lines(screen, blue, True, testPoints, 2)

    '''
    #this just draws blue circles (was used for testing)
    for points in testPoints:
        pygame.draw.circle(screen, blue, points,horizontalBisect)
    '''


    pygame.display.update()

    while True:
       for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 pygame.quit(); sys.exit();
